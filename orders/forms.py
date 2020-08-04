from django import forms
from .models import Order
from django.forms import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget


class OrderCreateForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['user', 'location', 'delivery_date']
