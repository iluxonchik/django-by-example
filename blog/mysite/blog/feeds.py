from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
    title = 'Just Another Blog'
    link = '/blog/'
    description = "Just another blog. A Django blog."

    # Retrives the objects to be included in the feed
    def items(self):
        return Post.published.all()[:5]

    # "item_title" and "item_description" retriveve each object returned by items()
    #  and return its title and description
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
