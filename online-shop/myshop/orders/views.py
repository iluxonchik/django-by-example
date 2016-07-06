from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            request.session['order_id'] = order.id  # store order id in session, so that it can be used in payment (to get the order price)
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})  # get rendered HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispositon'] = 'filename="order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response