import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from .filters import OrderFilter
from .list import ListFilteredMixin
from django.utils.decorators import method_decorator


@login_required(login_url='account_login')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order,
                           })
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@method_decorator(login_required(login_url='account_login'), name='dispatch')
class OrderListView(ListFilteredMixin, ListView):
    model = Order
    template_name = 'orders/order/list.html'
    filter_set = OrderFilter
    queryset = Order.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset().all()
        return super().get_queryset().filter(user=self.request.user)


@login_required(login_url='account_login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_item = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_item': order_item,
    }
    return render(request, 'orders/order/detail.html', context)
