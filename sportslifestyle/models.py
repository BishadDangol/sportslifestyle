from django.db import models


# Create your models here.
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    size = models.ManyToManyField(Size, blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)

    def __str__(self):
        return self.product.name


class User(models.Model):
    first_name = models.CharField(default='', max_length=50, blank=True)
    last_name = models.CharField(default='', max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(max_length=12, blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to='avatar')

    def __str__(self):
        return self.first_name


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
