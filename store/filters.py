from django.forms import Select

from .models import *
import django_filters


class ProductFilter(django_filters.FilterSet):
    type = django_filters.ModelChoiceFilter(queryset=Type.objects.all(),
                                            widget=Select(attrs={'style': 'max-width: 15em'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                                widget=Select(attrs={'style': 'max-width: 15em'}))

    class Meta:
        model = Product
        fields = ('type', 'category')
