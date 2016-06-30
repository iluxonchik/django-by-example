from django.http import HttpResponseBadRequest

def ajax_required(f):
    """
    Makes sure that the request is done via AJAX.
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
