from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^groups$', views.group),
    url(r'^register$', views.addUser),
    url(r'^login$', views.loginUser),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^register/group$', views.addGroup),
    url(r'^login/group$', views.loginGroup),
    url(r'^add_task$', views.add_task),
]
