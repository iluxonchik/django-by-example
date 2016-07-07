from .import views
from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    url(_(r'^done/$'), views.payment_done , name='done'),
    url(_(r'^cancelled/$'), views.payment_cancel , name='cancel'),
    url(_(r'^process/$'), views.payment_process , name='process'),
]