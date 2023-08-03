from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('my_orders/', views.my_orders_view, name='my_orders'),
    path('order_detail/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('create_order/', views.create_order_view, name='create_order'),
]
