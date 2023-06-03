from django.contrib import admin
from .models import Category, Product
from django.utils.safestring import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_category', 'slug_category']
    prepopulated_fields = {'slug_category': ('name_category', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name_product', 'slug', 'price_product', 'available', 'created', 'uploaded', 'image_show']
    list_filter = ['slug', 'price_product', 'created', 'uploaded']
    list_editable = ['price_product', 'available']
    prepopulated_fields = {'slug': ('name_product', )}


    def image_show(self, obj):
        if obj.image_product:
            return mark_safe("<img src='{}' width='60' />".format(obj.image_product.url))
        return "None"

    image_show.__name__ = "Картинка"
