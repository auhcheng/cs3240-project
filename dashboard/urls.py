from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.Dashboard),
    url(r'^profile/$', views.update_profile),
    url(r'^account/logout/$', views.Logout),
]