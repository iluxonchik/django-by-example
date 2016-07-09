import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class Recommender(object):
    """
    The idea is that there is a key-value store with the following content: {'product:XXX:purchased_wiht': {'other_product_id', num_times_bought_together, ...}} 
    """
    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought together
                if product_id != with_id:
                    # increment the score for products bought together
                    r.zincrby(self.get_product_key(product_id), with_id, amount=1)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in poroducts]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(self.get_product_key(product_id[0]), 0, -1, desc=True)[:max_results]
        else:
            # more than one product
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp{}'.format(flat_ids)

            # in this case we have multiple products, so let's combine all of their scores
            # and store the resulting set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove the ids of the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, in descendant order
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key, we don't need it anymore
            r.delete(tmp_key)

        suggested_product_ids = [int(id) for id in suggestions]

        # get suggested products and sort them in the order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
