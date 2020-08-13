from django.forms import DateInput, Select

from .models import *
import django_filters
from django_filters import FilterSet



class OrderFilter(FilterSet):
    delivery_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date', 'style': 'max-width: 15em'}))
    location = django_filters.ModelChoiceFilter(queryset=Location.objects.all(),widget=Select(attrs={'style': 'max-width: 15em'}))
    location__route = django_filters.ModelChoiceFilter(queryset=Route.objects.all(), widget=Select(attrs={'style': 'max-width: 15em'}))

    class Meta:
        model = Order
        fields = ('location', 'delivery_date', 'location__route')
