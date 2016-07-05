from .import views
from django.conf.urls import url

urlpatterns = [
    url(r'^done/$', views.payment_done , name='done'),
    url(r'^cancelled/$', views.payment_cancel , name='cancel'),
    url(r'^process/$', views.payment_process , name='process'),
]