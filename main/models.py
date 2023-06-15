from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import User
import stripe



stripe.api_key = settings.STRIPE_SECRET_KEY


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
    stripe_product_price_id = models.CharField(max_length=150, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name_product',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f'Продукт: {self.name_product} | Категория: {self.category.name_category}'

    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.id, self.slug])


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name_product)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price_product * 100), currency="rub"
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price_product * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name_product,
            'quantity': self.quantity,
            'price': float(self.product.price_product),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_crated = False
            return basket, is_crated
