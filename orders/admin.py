from django.contrib import admin
from .models import Location, Company, Order, OrderItem
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

admin.site.register(Location)
admin.site.register(Company)

admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'location', 'delivery_date',
                    'created', 'update', 'payment_status']
    list_filter = [('delivery_date', DateRangeFilter), 'location', 'user']
    inlines = [OrderItemInline]
