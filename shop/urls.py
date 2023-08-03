from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('<int:product_id>/', views.shop_detail_view, name='shop_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/apply_discount/', views.apply_discount, name='apply_discount'),
    path('cart/', views.cart_view, name='cart_view'),
    path('clean_cart/', views.clean_cart, name='clean_cart'),
    path('remove_cart/<int:pid>', views.remove_cart, name='remove_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('add_cart/', views.cart_add, name='add_cart'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('tag/<slug:slug>/', views.tag_view, name='tag'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('', views.shop_view, name='shop')
]