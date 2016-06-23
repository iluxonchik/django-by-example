from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

# simple_tag - process the data and return a string
@register.simple_tag
def total_posts():
    return Post.published.count()

# inclusion_tag - process the data and return a rendered template
#                 allows to render a template with the context variables that are returned by this function
# In this case it's going to render the 'latest_posts.html' template with the context returned by the function
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# assignment_tag - process the data and set a variable in the context
#                  it's like simple_tag, but it stores the result in a given variable 
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

