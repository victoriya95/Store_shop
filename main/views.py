from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import CartAddProductForm
from users.models import User
from django.views.generic.list import ListView


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'main/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'main/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})


def home_page(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'main/product/index.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


# @login_required
# def basket_add(request, product_id):
    # Basket.create_or_update(product_id, request.user)

    # return HttpResponseRedirect(request.META['HTTP_REFERER'])

#
# def basket_add(request, product_id):
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=request.user, product=product)
#
#     if not baskets.exists():
#         Basket.objects.create(user=request.user, product=product, quantity = 1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])
#
#
# def basket_remove(request, basket_id):
#     basket = Basket.objects.get(id=basket_id)
#     basket.delete()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])