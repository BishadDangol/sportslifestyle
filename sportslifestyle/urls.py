from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("shop", views.shop, name='shop'),
    path('product-detail/<slug>', views.product_detail, name='product-detail'),
    path("new-arrivals", views.new_arrivals, name='new-arrivals'),
    path("offer", views.offer, name='offer'),
    path("search", views.search, name='search'),
    path('category/<slug>', views.sort_category, name='category'),

    path("register", views.user_register, name='register'),
    path("login", views.user_login, name='login'),
    path("logout", views.user_logout, name='logout'),
    path("profile", views.profile, name='profile'),

    path("cart-view", views.cart_view, name='cart-view'),
    path("add-to-cart/<int:id>", views.add_to_cart, name='add-to-cart'),
    path("remove-from-cart/<int:id>", views.remove_from_cart, name='remove-from-cart'),
    path("increase-from-cart/<int:id>", views.increase_cart, name='increase-from-cart'),
    path("decrease-from-cart/<int:id>", views.decrease_cart, name='decrease-from-cart'),

    path("checkout", views.checkout, name='checkout'),
    path("ratings", views.ratings, name='ratings'),

    path("success", views.successpayment, name='success'),

]
