from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('create-payment/<int:order_id>/', views.create_payment, name='create_payment'),
    path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
] 