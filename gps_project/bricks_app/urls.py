from django.urls import path
from . import views


urlpatterns=[ 
    path('', views.dashboard, name='dashboard'),

    path('add_customer/', views.add_customer, name='add_customer'),
    path('list_customer/',views.list_customer, name='list_customer'),

    path('add_device/', views.add_device, name='add_device'),
    path('list_device/',views.list_device, name='list_device'),
    path('login', views.login_view, name='login'),
    path('products/', views.list_products, name='list-products'),
    path('orders/', views.list_orders, name='list_orders'),
    path('submit-order/', views.submit_order, name='submit_order'),

]