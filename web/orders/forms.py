from django import forms
from orders.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'email',
            'name',
            'phone',
            'district',
            'zipcode',
            'address',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }