from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CustomerForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.

def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        # check if user entered has existing username
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        user = User.objects.create_user(username=name, email=email, password=password)
        Customer.objects.create(user=user, contact=contact, )
        messages.success(request, 'Successfully registered')
        return redirect('login')
    else:
        data = {
            'form': CustomerForm()
        }
        return render(request, 'pages/register.html', data)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('login')

    data = {
        'form': AuthenticationForm()
    }
    return render(request, 'pages/login.html', data)


def user_logout(request):
    logout(request)
    return redirect('index')


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
    product_list = Product.objects.filter(category__slug=slug)
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


def profile(request):
    return render(request, 'pages/profile.html')
