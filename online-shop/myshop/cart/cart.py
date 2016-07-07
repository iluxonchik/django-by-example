from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart from a request instance
        """
        self.session = request.session  # we need to access the session in other methods
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}  # product_id: {quanity, price} --> gurantees that the same product isn't added more than once
        self.cart = cart
        self.__coupon_id = self.session.get('coupon_id')

    @property
    def coupon(self):
        if self.__coupon_id:
            return Coupon.objects.get(id=self.__coupon_id)
        return None

    def get_discount(self):
        if self.__coupon_id:
            return (self.coupon.discount / Decimal('100') * self.get_total_price())
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def add(self, product, quantity, update_quantity=False):
        product_id = str(product.id)  # we're using JSON to serialize the session data and it only allows string keys
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}  # product.price converted to string in order to serialize it
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified", to make sure it's saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from SESSION. NOTE: the cart is still present in self.cart after the 'del'
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        # NOTE: we're not saving the cart here, simply filling its items with
        # the required values and then yielding them

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])  # now we're not going to serialize it, so we'll convert it to Decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())