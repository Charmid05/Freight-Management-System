from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    re_path(r'^edituser/(?P<pk>[0-9]+)/$', views.edituser, name='edituser'),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    re_path(r'^makeadmin/(?P<pk>[0-9]+)/$', views.makeadmin, name='makeadmin'),
    re_path(r'^profile/(?P<pk>[0-9]+)/$', views.details, name='details'),
    path('adduser/', views.adduser, name='adduser'),
]
