from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("shop", views.shop, name='shop'),
    path('product-detail/<slug>', views.product_detail, name='product-detail'),
    path("search", views.search, name='search'),
    path('category/<slug>', views.sort_category, name='category'),

]
