from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^map/', views.map, name = 'map'),
    url(r'^add_location/', views.add_location, name = 'add_location'),
    url(r'^add_review/(\d+)/$', views.add_review, name = 'add_review'),
    url(r'^signup/', views.signup, name = 'signup'),
    url(r'^logout/', views.logout_view, name = 'logout_view'),
]