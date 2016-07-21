from django import template

register = template.Library()

# We need to access the model name in our templtes, this can be done by accessing
# the "_meta.model_name" attribute of the model, but we can't access attributes
# that begin with underscores in templates, so we create a template tag instead.
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None