from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_category', 'slug_category']
    prepopulated_fields = {'slug_category': ('name_category', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name_product', 'slug', 'price_product', 'available', 'created', 'uploaded']
    list_filter = ['slug', 'price_product', 'created', 'uploaded']
    list_editable = ['price_product', 'available']
    prepopulated_fields = {'slug': ('name_product', )}

