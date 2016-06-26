from django.conf.urls import url
from . import views

urlpatterns = [
    # previous, hand-made login view
    # url(r'^login/$', views.user_login, name='login'),

    # Using Django's built-in authentication views
    # Django expects the authentication templates to be within the "templates/registration" directory of the app
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'), 
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    # logout-then-login does not need a template, since it performs a redirect to the login view
    url(r'^logut-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^dahsboard/$', views.dashboard, name='dashboard') 
]