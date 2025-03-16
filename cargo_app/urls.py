from django.urls import path, re_path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.addshipment, name='addshipment'),
    re_path(r'^(?P<pk>\d+)/$', views.details, name='details'),
    re_path(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    path('gettrack/', views.gettrack, name='gettrack'),
    path('getcorporatetrack/', views.getcorporatetrack, name='getcorporatetrack'),
    re_path(r'^user/(?P<pk>[0-9]+)/$', views.listUserShipments, name='listUserShipments'),
    path('categories/', views.sendCategories, name='sendCategories'),
    path('shiporder/', views.shipOrder, name='shipOrder'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
