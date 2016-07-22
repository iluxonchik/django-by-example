from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.StudentRegstrationView.as_view(), name='student_registration'),
]
