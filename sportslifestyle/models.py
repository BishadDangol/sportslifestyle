from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='photos/customers', blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    Variants = (
        ('None', 'None'),
        ('Size', 'Size'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    variants = models.CharField(max_length=100, choices=Variants, default='None')
    discount = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('OnShipping', 'OnShipping'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    total = models.FloatField()
    status = models.CharField(choices=STATUS, default='New', max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class Review(models.Model):
#     RATING_CHOICES = (
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#     )
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     pub_date = models.DateTimeField('date published')
#     comment = models.CharField(max_length=200)
#     rating = models.IntegerField(choices=RATING_CHOICES)
#
#     def __str__(self):
#         return self.rating


class Return(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='photos/return', blank=True, null=True)
    return_desc = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    news_desc = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.news_desc
