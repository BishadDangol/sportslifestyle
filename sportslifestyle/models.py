from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='photos/customers', blank=True, null=True)

    def __str__(self):
        return self.user.username


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
    # Variants = (
    #     ('None', 'None'),
    #     ('Size', 'Size'),
    # )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    # variants = models.CharField(max_length=100, choices=Variants, default='None')
    discount = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    # find discount price for display
    def dis_price(self):
        return self.price - self.discount

    # find total number of reviews in product
    def total_review(self):
        return self.comment_set.count()

    # find avg number of rating in product
    def avg_rating(self):
        total = 0
        for comment in self.comment_set.all():
            total += comment.rating
        if total > 0:
            return total / self.total_review()
        else:
            return 0


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


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)

    def total_discount(self):
        total = 0
        for cart in self.cartdetail_set.all():
            if cart.product.discount:
                total += cart.product.discount * cart.quantity
            else:
                total += 0
        return total

    def total_price(self):
        return self.total - self.total_discount()

    def tax_amount(self):
        pp = float(self.total_price())
        return pp * 0.13

    def grand_total(self):
        tt = float(self.total_price())
        ta = float(self.tax_amount())
        return tt + ta

    def get_product_name(self):
        return self.cartdetail_set.all()[0].product.name


class CartDetail(models.Model):
    unique_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    sub_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"({self.variant.size.name})"


class Order(models.Model):
    order_status = (
        ("Order Received", "Order Received"),
        ("Processing", "Processing"),
        ("On shipping", "On shipping"),
        ("Completed", "Completed"),
        ("Order Canceled", "Order Canceled"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    unique_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=order_status, default='Order Received')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address_optional = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    optional_phone = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    total = models.PositiveIntegerField(default=0)

    loop_order_status = list(order_status)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        return self.unique_cart.total_price()

    def get_cart_items(self):
        return self.unique_cart.cartdetail_set.all().count()

    def get_cart_discount(self):
        return self.unique_cart.total_discount()

    def get_tax_amount(self):
        return self.unique_cart.tax_amount()

    def get_grand_total(self):
        return self.unique_cart.grand_total()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
