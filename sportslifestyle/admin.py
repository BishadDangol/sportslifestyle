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


admin.site.register(Return)
admin.site.register(Newsletter)
