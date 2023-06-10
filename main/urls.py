from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [

    path('', views.home_page, name='home_page'),

    path('product_list', views.product_list, name='product_list'),

    path('<int:id>/<slug:slug_category>/', views.product_list,
         name='product_list_by_category'),

    path('<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
