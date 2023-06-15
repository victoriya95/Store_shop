from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplates, OrderListView, OrderDetailView


app_name = 'orders'

urlpatterns = [

    path('', OrderListView.as_view(), name='orders_list'),
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_cancel/', CanceledTemplates.as_view(), name='order_cancel'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),




]
