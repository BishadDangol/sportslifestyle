import csv

from django.contrib.sites import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from .forms import CustomerForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests


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
    sort_order = request.GET.get('sort', '-id')  # Get the sort order from the query string
    product_list = Product.objects.exclude(discount__gt=0).order_by(sort_order)  # Get products with no discount

    paginator = Paginator(product_list, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)
    page_obj.sort_order = sort_order  # add sort_order to page_obj
    # Construct the filter option links with the current sort order
    filter_links = [
        ('Date Added (New to Old)', f"{reverse('shop')}?sort=-id"),
        ('Date Added (Old to New)', f"{reverse('shop')}?sort=id"),
        ('Price (High to Low)', f"{reverse('shop')}?sort=-price"),
        ('Price (Low to High)', f"{reverse('shop')}?sort=price"),

    ]
    for i, link in enumerate(filter_links):
        filter_links[i] = (link[0], f"{link[1]}&page={page_number}" if page_number else link[1])

    data = {
        'productData': page_obj,
        'title': 'Shop',
        'sortOrder': sort_order,
        'filterLinks': filter_links,
    }
    # return HttpResponse(page_obj)
    return render(request, 'pages/shop.html', data)


def search(request):
    # storing entered words in keyword variable
    keyword = request.GET.get('search')
    # filtering keyword in models
    product_list = Product.objects.filter(
        Q(name__icontains=keyword) | Q(description__icontains=keyword))  # icontains checks case-sensitive
    # paginator = Paginator(product_list, 5)  # Show 5 products per page.
    # page_number = request.GET.get('page')  # get number of page
    # page_obj = paginator.get_page(page_number)
    data = {
        'productData': product_list,
        'result': keyword,
    }
    return render(request, 'pages/search.html', data)


def sort_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category__slug=slug).order_by('-id')
    paginator = Paginator(product_list, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)
    data = {
        'productData': page_obj,
        'catName': category.name
    }
    return render(request, 'pages/category.html', data)


def product_detail(request, slug):
    get_product = Product.objects.get(slug=slug)
    cat_id = get_product.category.id
    similar_products = Product.objects.filter(category__id=cat_id).exclude(id=get_product.id).order_by('-id')
    data = {
        'productData': Product.objects.get(slug=slug),
        'similarData': similar_products[0:4],
    }
    return render(request, 'pages/product-detail.html', data)


def add_to_cart(request, id):
    get_product = Product.objects.get(id=id)
    cart_session_key = request.session.get('cart_unique_key', None)
    # if form is used to add to cart
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        get_v = request.POST.get('variant')
        variant = ProductVariant.objects.get(id=get_v)
        if variant.quantity < int(quantity):
            messages.error(request, 'Sorry! We have only ' + str(variant.quantity) + ' Products in left')
            back = request.META.get('HTTP_REFERER')
            return redirect(back)

        else:
            # if session key exist
            if cart_session_key:
                unique_key = Cart.objects.get(id=cart_session_key)
                try:
                    # if product already exists in cart
                    cart_product = CartDetail.objects.get(unique_cart=unique_key, product=get_product, variant=variant)
                    cart_product.quantity = cart_product.quantity + int(quantity)
                    cart_product.total = cart_product.sub_total * cart_product.quantity
                    cart_product.save()
                    unique_key.total = unique_key.total + (get_product.price * int(quantity))
                    unique_key.save()
                    back = request.META.get('HTTP_REFERER')
                    return redirect(back)
                except CartDetail.DoesNotExist:
                    # new product added in the cart
                    cart_product = CartDetail.objects.create(
                        unique_cart=unique_key,
                        product=get_product,
                        quantity=quantity,
                        total=get_product.price * int(quantity),
                        sub_total=get_product.price,
                        variant=variant)
                    cart_product.save()
                    unique_key.total = unique_key.total + (get_product.price * int(quantity))
                    unique_key.save()
                    back = request.META.get('HTTP_REFERER')
                    return redirect(back)
            else:
                # creates a new session key
                unique_key = Cart.objects.create()
                request.session['cart_unique_key'] = unique_key.id
                cart_product = CartDetail.objects.create(
                    unique_cart=unique_key,
                    product=get_product,
                    quantity=quantity,
                    total=get_product.price * int(quantity),
                    sub_total=get_product.price,
                    variant=variant)
                cart_product.save()
                unique_key.total = unique_key.total + (get_product.price * int(quantity))
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
        # check if cart is empty
        if unique_key.cartdetail_set.count() == 0:
            return render(request, 'pages/empty.html')
        else:
            data = {
                # filters each product in CartDetail related to single Cart model
                'cartData': CartDetail.objects.filter(unique_cart=unique_key),
                'uniqueKey': unique_key
            }
        return render(request, 'pages/cart.html', data)
    else:
        return render(request, 'pages/cart.html')


def remove_from_cart(request, id):
    # Retrieve the CartDetail object with the specified ID
    cart_product_object = CartDetail.objects.get(id=id)
    # Retrieve the Cart object associated with the CartDetail object
    cart = cart_product_object.unique_cart
    cart.total -= cart_product_object.sub_total
    cart.save()

    # Remove the CartDetail object from the database
    cart_product_object.delete()

    # Loop over all the CartDetail objects in the cart and calculate the new total
    new_total = 0
    for item in cart.cartdetail_set.all():
        new_total += item.sub_total
    cart.total = new_total
    cart.save()

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

    messages.success(request, "Cart was successfully updated")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        # if payment method is cash
        if request.POST['paymentMethod'] == 'cash':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            full_name = first_name + ' ' + last_name
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            phone_optional = request.POST.get('phone_optional')
            address = request.POST.get('address')
            address_optional = request.POST.get('address_optional')
            city = request.POST.get('city')
            product_unique_cart_id = request.session.get('cart_unique_key')
            cat_obj = Cart.objects.get(id=product_unique_cart_id)
            order_object = Order.objects.create(
                full_name=full_name,
                email=email,
                address=address,
                address_optional=address_optional,
                phone=phone,
                optional_phone=phone_optional,
                city=city,
                total=cat_obj.total,
                unique_cart=Cart.objects.get(id=cat_obj.id),
                customer=Customer.objects.get(user=request.user)
            )
            order_object.save()
            del request.session['cart_unique_key']
            return redirect('index')
        # if payment method is khalti
        else:
            product_unique_cart_id = request.session.get('cart_unique_key')
            cat_obj = Cart.objects.get(id=product_unique_cart_id)
            total_price = int(cat_obj.grand_total())
            total = total_price * 100

            data = {
                "return_url": "http://127.0.0.1:8000/success",
                "website_url": "https://example.com/",
                "amount": total,
                "purchase_order_id": "test12",
                "purchase_order_name": "test",
            }
            headers = {
                "Authorization": "Key 93a09b1c580c4496a040e1a92a6e349d"

            }
            response = requests.post("https://a.khalti.com/api/v2/epayment/initiate/", json=data, headers=headers)
            print(response, response.text)
            data = response.json()
            # if payment successful
            if response.status_code == 200:
                a = response.json()
                pdi = a.get('pidx')
                url = "https://a.khalti.com/api/v2/payment/verify/"

                payload = {
                    'token': pdi,
                    'amount': total
                }
                ver_Header = {
                    'Authorization': 'Key 93a09b1c580c4496a040e1a92a6e349d'
                }
                resTest = requests.request("POST", url, headers=ver_Header, data=payload)
                print(resTest, resTest.text)

                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                full_name = first_name + ' ' + last_name
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                phone_optional = request.POST.get('phone_optional')
                address = request.POST.get('address')
                address_optional = request.POST.get('address_optional')
                city = request.POST.get('city')
                product_unique_cart_id = request.session.get('cart_unique_key')
                cat_obj = Cart.objects.get(id=product_unique_cart_id)
                order_object = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    address=address,
                    address_optional=address_optional,
                    phone=phone,
                    optional_phone=phone_optional,
                    city=city,
                    total=cat_obj.total,
                    unique_cart=Cart.objects.get(id=cat_obj.id),
                    customer=Customer.objects.get(user=request.user)
                )
                order_object.save()
                del request.session['cart_unique_key']
                return HttpResponseRedirect(data.get("payment_url"))

            else:
                messages.error(request, "Something went wrong")
                back = request.META.get('HTTP_REFERER')
                return redirect(back)

    else:
        product_session_key = request.session.get('cart_unique_key', None)
        # check if session key exist
        if product_session_key:
            cart = Cart.objects.get(id=product_session_key)
            # find if cart is empty or not
            if cart.cartdetail_set.count() == 0:
                return redirect('index')
            else:
                return render(request, 'pages/checkout.html')

        else:
            return redirect('index')


@login_required(login_url='login')
def profile(request):
    # Get the ID of the current user
    profile_id = request.user.id
    data = {
        # Retrieve all the Order objects associated with the Customer object
        # corresponding to the current user
        'ordersData': Order.objects.filter(customer=Customer.objects.get(user=profile_id)),
        'title': 'Profile'
    }
    return render(request, 'pages/profile.html', data)


def offer(request):
    product_list = Product.objects.all()  # Get products with no discount
    paginator = Paginator(product_list, 100)  # Show 5 products per page.
    page_number = request.GET.get('page')  # get number of page
    page_obj = paginator.get_page(page_number)

    data = {
        'productData': page_obj,
        'title': 'Offers',

    }
    return render(request, 'pages/offer.html', data)


def ratings(request):
    if request.method == 'POST':
        # Get the review, rating, and product ID from the POST request.
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        product_id = request.POST.get('product_id')
        # Retrieve the product object using the product ID.
        product = Product.objects.get(id=product_id)
        # Retrieve the authenticated user using the request object.
        auth_user = request.user.id
        auth = User.objects.get(id=auth_user)
        # Check if there is an existing comment object for this user and product
        if Comment.objects.filter(user=auth, product=product).exists():
            # If there is an existing comment object, update its review and ratings.
            comment_ojb = Comment.objects.get(user=auth, product=product)
            comment_ojb.review = review
            comment_ojb.rating = rating
            comment_ojb.save()
            all_ratings = Comment.objects.all()
            with open('ratings.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'user_id', 'product_id', 'rating'])
                for i in all_ratings:
                    writer.writerow([i.id, i.user.id, i.product.id, i.rating])
            messages.success(request, "Comment was successfully updated")
            # Redirect the user back to the referring page with a success message.
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            # If there is no existing comment object, create a new one.
            review = Comment.objects.create(
                product=product,
                review=review,
                rating=rating,
                user=auth
            )
        review.save()
        all_ratings = Comment.objects.all()
        # write csv file
        with open('ratings.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'product_id', 'rating'])
            for i in all_ratings:
                writer.writerow([i.id, i.user.id, i.product.id, i.rating])
        messages.success(request, "Comment was successfully added")
        # Redirect the user back to the referring page with a success message.
        return redirect(request.META.get('HTTP_REFERER'))


def successpayment(request):
    data = {

        'title': 'Success',

    }
    return render(request, 'pages/order-sucess.html', data)
