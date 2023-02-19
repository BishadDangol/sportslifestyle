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
        'productData': Product.objects.order_by('-id'),  # for displaying product by recently added
        'clothingData': Product.objects.filter(category__slug='clothing').order_by('-id'),  # display by clothing
        'shoeData': Product.objects.filter(category__slug='shoes').order_by('-id'),  # display by shoes
    }
    return render(request, 'pages/index.html', data)


def new_arrivals(request):
    product_list = Product.objects.order_by('-id')  # for displaying product by recently added
    paginator = Paginator(product_list, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)
    data = {
        'productData': page_obj,
        'title': 'Latest',
    }
    return render(request, 'pages/latest.html', data)


def shop(request):
    product_list = Product.objects.order_by('-id')
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
    product_list = Product.objects.filter(category__slug=slug).order_by('-id')
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


def add_to_cart(request, id):
    get_product = Product.objects.get(id=id)
    cart_session_key = request.session.get('cart_unique_key', None)
    # if session key exist
    if cart_session_key:
        unique_key = Cart.objects.get(id=cart_session_key)
        try:
            # if product already exists in cart
            cartproduct = CartDetail.objects.get(unique_cart=unique_key, product=get_product)
            cartproduct.quantity = cartproduct.quantity + 1
            cartproduct.total = cartproduct.sub_total * cartproduct.quantity
            cartproduct.save()
            unique_key.total = unique_key.total + get_product.price
            unique_key.save()
            back = request.META.get('HTTP_REFERER')
            return redirect(back)

        # new product when added in cart
        except CartDetail.DoesNotExist:
            cartproduct = CartDetail.objects.create(
                unique_cart=unique_key,
                product=get_product,
                quantity=1,
                total=get_product.price,
                sub_total=get_product.price)
            cartproduct.save()
            unique_key.total = unique_key.total + get_product.price
            unique_key.save()
            back = request.META.get('HTTP_REFERER')
            return redirect(back)

    # creates a new session key
    else:
        unique_key = Cart.objects.create(total=0)
        request.session['cart_unique_key'] = unique_key.id
        cartproduct = CartDetail.objects.create(
            unique_cart=unique_key,
            product=get_product,
            quantity=1,
            total=get_product.price,
            sub_total=get_product.price)
        cartproduct.save()
        unique_key.total = unique_key.total + get_product.price
        unique_key.save()
        back = request.META.get('HTTP_REFERER')
        return redirect(back)


def cart_view(request):
    # check if user has session key
    cart_session_key = request.session.get('cart_unique_key', None)
    # if user has session key and products present
    if cart_session_key:
        # finds cart owner with relation to session key
        unique_key = Cart.objects.get(id=cart_session_key)
        data = {
            # filters each product in CartDetail related to single Cart model
            'cartData': CartDetail.objects.filter(unique_cart=unique_key),
            'uniqueKey': unique_key
        }
        return render(request, 'pages/cart.html', data)
    # if user has no session key empty cart
    else:
        return render(request, 'pages/cart.html')


def remove_from_cart(request, id):
    # Retrieve the CartDetail object with the specified ID
    cart_product_object = CartDetail.objects.get(id=id)
    # Retrieve the Cart object associated with the CartDetail object
    cart = cart_product_object.unique_cart
    cart.total -= cart_product_object.sub_total
    cart.save()
    # Delete the CartDetail object from the database
    cart_product_object.delete()
    messages.success(request, "Items successfully deleted from cart")
    return redirect(request.META.get('HTTP_REFERER'))


def increase_cart(request, id):
    cart_product = CartDetail.objects.get(id=id)
    cart = cart_product.unique_cart
    cart.total += cart_product.sub_total
    cart.save()
    cart_product.quantity += 1
    cart_product.total = cart_product.sub_total * cart_product.quantity
    cart_product.save()
    messages.success(request, "Cart was successfully updated")
    return redirect(request.META.get('HTTP_REFERER'))


# def decrease_cart(request, id):
#     cart_product = CartDetail.objects.get(id=id)
#     cart = cart_product.unique_cart
#     cart.total -= cart_product.sub_total
#     cart.save()
#     if cart_product.quantity > 1:
#         cart_product.quantity -= 1
#         cart_product.total = cart_product.sub_total * cart_product.quantity
#         cart_product.save()
#
#         # Update the corresponding Cart object's total
#         cart_details = cart.cartdetail_set.all()
#         cart.total = sum(detail.total for detail in cart_details)
#         cart.save()
#     messages.success(request, "Cart was successfully updated")
#     return redirect(request.META.get('HTTP_REFERER'))

def decrease_cart(request, id):
    cart_product = CartDetail.objects.get(id=id)
    cart = cart_product.unique_cart
    cart.total -= cart_product.sub_total
    cart.save()
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.total = cart_product.sub_total * cart_product.quantity
        cart_product.save()
    else:
        cart_product.delete()  # Remove the cart detail if the quantity is 1 or less

    # Update the corresponding Cart object's total and cart details count
    cart_details = cart.cartdetail_set.all()
    cart.total = sum(detail.total for detail in cart_details)
    cart.cart_details_count = len(cart_details)
    cart.save()

    messages.success(request, "Cart was successfully updated")
    return redirect(request.META.get('HTTP_REFERER'))
