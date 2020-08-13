import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_localflavor_us.models import USStateField
from phone_field import PhoneField

from store.models import Product


# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Address(models.Model):
    label = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = USStateField(default="OH")
    zip_code = models.IntegerField()

    def __str__(self):
        return self.label


class Location(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    store_Number = models.CharField(max_length=10, blank=True, null=True)
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_number = PhoneField(blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


def increment_order_id():
    """ Creates Order ID of format  ABCD  . Change as per neeed."""
    prefix = 'ABCD'
    # if you are gonna change it but its not 4 character long
    # make sure to change the numbers below too
    last_order = Order.objects.all().order_by('id').last()
    if not last_order:
        return str(prefix) + str(datetime.date.today().year) + str(
            datetime.date.today().month).zfill(2) + str(
            datetime.date.today().day).zfill(2) + '0000'
    order_id = last_order.order_id
    order_id_int = int(order_id[12:16])
    new_order_id_int = order_id_int + 1
    new_order_id = str(prefix) + str(str(datetime.date.today().year)) + str(
        datetime.date.today().month).zfill(2) + str(
        datetime.date.today().day).zfill(2) + str(new_order_id_int).zfill(4)
    return new_order_id


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, default=increment_order_id, null=True, blank=True, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING, null=True, blank=True)
    delivery_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('-delivery_date',)

    def __str__(self):
        return f'Order {self.id}'

    def get_absolute_url(self):
        return reverse('orders:order_detail',
                       args=[self.order_id])

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def count_items(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='items')
    description = models.CharField(max_length=500, blank=True)
    # Item
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1, null=False)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
