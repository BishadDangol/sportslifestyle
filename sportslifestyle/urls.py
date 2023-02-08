from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('product-detail/<slug>', views.product_detail, name='product-detail'),

]
