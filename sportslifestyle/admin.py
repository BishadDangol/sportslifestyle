from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.html import format_html


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# add multiple product in same page for admin
class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 5


# add multiple product Variant same page for admin
class ProductVariantInLine(admin.TabularInline):
    model = ProductVariant
    extra = 5


@admin.register(Size)
class AdminProductImage(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'is_available', 'status', 'get_image']
    list_editable = ['price', 'is_available', 'status']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    inlines = [ProductImageInLine, ProductVariantInLine]
    search_fields = ['name', 'price', 'is_available', 'status']

    # display product image in admin panel
    def get_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        else:
            return None


@admin.register(ProductImage)
class AdminProductImage(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_per_page = 20


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    pass


@admin.register(CartDetail)
class CartDetailAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin site
    list_display = ('unique_cart', 'product', 'quantity', 'total', 'size',)

    # Define a custom method to display the size name in the list view
    def size(self, obj):
        if obj.variant:
            # If a variant is selected, display the size name
            return obj.variant.size.name
        else:
            # If no variant is selected, display a dash (-)
            return "-"

    # Set the admin_order_field attribute to allow sorting by size name
    size.admin_order_field = 'variant__size__name'


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['customer', 'total', 'status']
    list_editable = ['status']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'review']


admin.site.register(Return)
admin.site.register(Newsletter)
