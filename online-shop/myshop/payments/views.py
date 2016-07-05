from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from orders.models import Order
from decimal import Decimal
from django.utils.safestring import mark_safe

import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox, 
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = order.get_total_cost().quantize(Decimal('0.1'))
    if request.method == 'POST':
        # Get payment nonce and process payment
        client_nonce = request.POST.get('payment_method_nonce')
        if client_nonce is None:
            # no client nonce
            request.session['message'] = 'Error getting client nonce'
            return redirect(reverse('payments:cancel'))

        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_nonce': client_nonce,
            'options': {
            'submit_for_settlement' : True,
            }
        })

        if result.is_success:
            # all good, redirect to success page
            return redirect('payments:done')
        else:
            # something went wrong, build the error message and redirect
            message = ''
            for error in result.errors.deep_errors:
                message += error.message 

            message = '<p>' + message + '</p>'
            request.session['message'] = message
            return redirect(reverse('payments:cancel'))


    else:
        # Generate client token
        client_token = braintree.ClientToken.generate()
        return render(request, 'payments/process.html', {'client_token': client_token, 'amount' : amount})

def payment_cancel(request):
    message = request.session.get('message')  # quick hack: in case of an error message, it's set in the session (to avoid passing in url)
    if message:
        message = mark_safe(message)
        del request.session['message']
    return render(request, 'payments/cancelled.html', {'message': message})

def payment_done(request):
    return render(request, 'payments/done.html')
