from django.conf.urls import url
from . import views
from django.conf.urls import url, include 

urlpatterns = [
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='home'),
    url(r'^googleLogin$', views.googleLogin, name='googleLogin'),
    url(r'^groups$', views.group),
    url(r'^register$', views.addUser),
    url(r'^login$', views.loginUser, name='login'),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^register/group$', views.addGroup),
    url(r'^login/group$', views.loginGroup),
    url(r'^add_task$', views.add_task),
    url(r'^view$', views.view),
    url(r'^new_todo$', views.new_todo),
    url(r'^add_todo$', views.add_todo),
]
