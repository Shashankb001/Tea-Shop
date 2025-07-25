from django.urls import path
from . import views

app_name = 'orders'
 
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order-confirmation'),
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
] 