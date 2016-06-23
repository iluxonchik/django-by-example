from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    # the attributes below can also be methods
    changefreq = 'weekly'
    priority = 0.9

    # returns the QuerySet of objects to include in the sitemap. By default, Django calls get_absoulte_url() on 
    # each object of the QuerySet. As an alternative, "location" method can be specified.
    # Default implementation of location():
    #
    #     def location(self, obj):
    #         return obj.get_absolute_url()
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish