from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdminView(admin.ModelAdmin):
    list_display = ['id', 'owner', 'address', 'total_price', 'discount_percent',
                    'end_price', 'created', 'updated', 'paid']
    list_display_links = ['address', 'total_price', 'discount_percent',
                          'end_price', 'created', 'updated']
    list_filter = ['owner']


class OrderItemAdminView(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'unit_price', 'quantity']
    list_display_links = ['id', 'unit_price', 'quantity']
    list_filter = ['order']


admin.site.register(Order, OrderAdminView)
admin.site.register(OrderItem, OrderItemAdminView)

