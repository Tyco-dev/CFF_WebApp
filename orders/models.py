import uuid, datetime
from decimal import Decimal
from phone_field import PhoneField
from store.models import Product
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    store_Number = models.CharField(max_length=10, blank=True, null=True)
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_number = PhoneField(blank=True, null=True)

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
    NOTPAID = 0
    PAID = 1
    PARTPAID = 2

    PAYMENT_STATUS = (
        (NOTPAID, 'Not Paid'),
        (PARTPAID, 'Partial Paid'),
        (PAID, 'Paid'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, default=increment_order_id, null=True, blank=True, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    payment_status = models.IntegerField(default=NOTPAID, choices=PAYMENT_STATUS, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('-created', '-id')

    def __str__(self):
        return '%s' % (self.order_id)

    def subtotal(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.subtotal()).quantize(Decimal('0.01'))
        return str(total)

    def total(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.total()).quantize(Decimal('0.01'))

        return str(total - self.discount)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='orderitems', null=True)
    desc = models.CharField(max_length=500, null=True)
    # Item
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Records
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.id)

    def description(self):
        # If items is linked, return item's description
        if self.product:
            return str(self.product.name)
        else:
            return 'Order Item'

    def subtotal(self):
        total = ((self.price * Decimal(self.quantity)).quantize(
            Decimal('0.01')) - self.discount)
        return str(total)

    def taxtotal(self):
        subtotal = Decimal(self.subtotal()).quantize(Decimal('0.01'))
        total = subtotal
        return str(Decimal(total).quantize(Decimal('0.01')))

    def total(self):
        total = Decimal(self.subtotal()).quantize(Decimal('0.01')).quantize(Decimal('0.01'))
        return str(total)
