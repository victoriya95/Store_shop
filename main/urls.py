from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.product_list, name='product_list'),

    path('<int:id>/<slug:slug_category>/', views.product_list,
         name='product_list_by_category'),

    path('<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),




]
