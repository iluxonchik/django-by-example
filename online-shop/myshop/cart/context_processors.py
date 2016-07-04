from .cart import Cart

# CONTEXT PROCESSOR
# -----------------
# A context processor is a Python function that takes the request object as argument and 
# returns a dictionary that gets added to the request context


def cart(request):
    return {'cart': Cart(request) }
