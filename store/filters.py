from .models import *
import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('type', 'category')