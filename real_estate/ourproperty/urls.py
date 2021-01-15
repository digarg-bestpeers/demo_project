from django.urls import path
from django.conf.urls import url
from ourproperty import views


urlpatterns = [
    path('', views.dealer_property, name='dealer_property_detail'),
    url(r'^(?P<dealer_key>\w{1,10})/$', views.public_properties, name='public_properties'),
    url(r'^(?P<dealer_key>\w{1,10})/payment/$', views.payment, name='payment'),

]
