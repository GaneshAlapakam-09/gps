from django.urls import path
from . import views


urlpatterns=[ 
    path('', views.dashboard, name='dashboard'),

    path('add_customer/', views.add_customer, name='add_customer'),
    path('list_customer/',views.list_customer, name='list_customer'),

    path('add_device/', views.add_device, name='add_device'),
    path('list_device/',views.list_device, name='list_device'),

]