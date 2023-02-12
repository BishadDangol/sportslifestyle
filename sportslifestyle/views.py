from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.

def index(request):
    data = {
        'productData': Product.objects.order_by('-id')  # for displaying product by recently added
    }
    return render(request, 'pages/index.html', data)


def shop(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)
    data = {
        'productData': page_obj,
        'title': 'Shop',
    }
    # return HttpResponse(page_obj)
    return render(request, 'pages/shop.html', data)


def search(request):
    # if search is done from post method
    if request.method == "POST":
        # storing entered words in keyword variable
        keyword = request.POST['search']
        # filtering keyword in models
        product_list = Product.objects.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword))  # icontains checks case-sensitive
        paginator = Paginator(product_list, 5)  # Show 5 products per page.
        page_number = request.GET.get('page')  # get number of page
        page_obj = paginator.get_page(page_number)
        data = {
            'productData': page_obj,
            'result': keyword,
        }
        return render(request, 'pages/shop.html', data)
    else:

        return redirect('index')


def sort_category(request, slug):
    product_list = Product.objects.filter(category__slug=slug)  # icontains checks case-sensitive
    paginator = Paginator(product_list, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)
    data = {
        'productData': page_obj,
    }
    return render(request, 'pages/shop.html', data)


def product_detail(request, slug):
    data = {
        'productData': Product.objects.get(slug=slug)
    }
    return render(request, 'pages/product-detail.html', data)
