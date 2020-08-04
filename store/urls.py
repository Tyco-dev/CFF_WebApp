from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<slug:type_slug>/', views.product_list, name='product_list_by_type'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]