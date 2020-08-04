from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, View
from .models import Product, Category, Type
from .filters import ProductFilter
from cart.forms import CartAddProductForm

# Create your views here.
def home(request):
    context = {}
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=Product.objects.all())
    products = myFilter.qs
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'myFilter': myFilter,
    }

    return render(request, 'store/product/product_list.html', context)


def product_detail(request, id, slug):
    # uses Id and SLUG to retrieve Product instance.
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'store/product/product_detail.html', context)
