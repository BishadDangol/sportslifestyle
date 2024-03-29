# Generated by Django 4.1.5 on 2023-01-29 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/category')),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_desc', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/products')),
                ('is_available', models.BooleanField(default=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('discount', models.IntegerField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportslifestyle.category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=50)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=12, null=True)),
                ('avatar', models.ImageField(blank=True, upload_to='avatar')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user_name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=200)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sportslifestyle.product')),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('surname', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/return')),
                ('return_desc', models.TextField(blank=True, max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportslifestyle.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/products')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportslifestyle.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('surname', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('OnShipping', 'OnShipping'), ('Delivered', 'Delivered')], default='New', max_length=15)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportslifestyle.user')),
            ],
        ),
    ]
