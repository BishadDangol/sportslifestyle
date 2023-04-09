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
    path('newsletter', views.custom_mail, name='newsletter'),

    path("register", views.user_register, name='register'),
    path("login", views.user_login, name='login'),
    path("logout", views.user_logout, name='logout'),
    path("profile", views.profile, name='profile'),
    path('password-reset', views.password_reset, name='password_reset'),
    path('password-reset-confirm/<token>', views.password_reset_confirm, name='password-reset-confirm'),

    path("cart-view", views.cart_view, name='cart-view'),
    path("add-to-cart/<int:id>", views.add_to_cart, name='add-to-cart'),
    path("remove-from-cart/<int:id>", views.remove_from_cart, name='remove-from-cart'),
    path("increase-from-cart/<int:id>", views.increase_cart, name='increase-from-cart'),
    path("decrease-from-cart/<int:id>", views.decrease_cart, name='decrease-from-cart'),

    path("checkout", views.checkout, name='checkout'),
    path("ratings", views.ratings, name='ratings'),

    path("success", views.successpayment, name='success'),

    path('admin-login', views.admin_login, name='admin-login'),
    path('admin-logout', views.admin_logout, name='admin-logout'),
    path('admin-panel', views.admin_panel, name='admin-panel'),
    path('add-product', views.add_product, name='add-product'),
    path('admin-product-list', views.admin_product_list, name='admin-product-list'),
    path('admin-user-list', views.admin_user_list, name='admin-user-list'),
    path('admin-product-delete/<int:id>', views.admin_product_delete, name='admin-product-delete'),
    path('admin-order-list', views.admin_order_list, name='admin-order-list'),
    path('admin-email', views.admin_email, name='admin-email'),

]
