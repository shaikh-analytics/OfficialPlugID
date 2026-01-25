from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('payment_method/', views.payment_method, name='payment_method'),
    path('crypto_payment/', views.crypto_payment, name='crypto_payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
