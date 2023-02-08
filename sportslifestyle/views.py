from django.shortcuts import render
from .models import *


# Create your views here.

def index(request):
    data = {
        'productData': Product.objects.all()
    }
    return render(request, 'pages/index.html', data)


def product_detail(request, slug):
    data = {
        'productData': Product.objects.get(slug=slug)
    }
    return render(request, 'pages/product-detail.html', data)