from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from main.views import basket_add, basket_remove

app_name = 'main'

urlpatterns = [

    path('', views.home_page, name='home_page'),

    path('product_list', views.product_list, name='product_list'),

    path('<int:id>/<slug:slug_category>/', views.product_list,
         name='product_list_by_category'),

    path('<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),

    # path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    # path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
