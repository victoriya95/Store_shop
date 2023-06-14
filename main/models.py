from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import User


class Category(models.Model):
    name_category = models.CharField(max_length=100, db_index=True)
    slug_category = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name_category',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        index_together = (('id', 'slug_category'),)

    def __str__(self):
        return self.name_category

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.id, self.slug_category])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    name_product = models.CharField(max_length=150, db_index=True)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    image_product = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description_product = models.TextField(max_length=1000, blank=True)
    price_product = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name_product',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f'Продукт: {self.name_product} | Категория: {self.category.name_category}'

    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.id, self.slug])


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)



class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name_product}'


    def sum(self):
        return self.product.price_product * self.quantity
