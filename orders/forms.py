from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'shipping_address', 'social_media_link', 'country', 'state', 'city', 'order_note']
