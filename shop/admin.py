from typing import Any, Optional
from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Question, Discount, ProductImage, Wishlist


class ProductTabular(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image.exists():
            return format_html(f'<img src="{obj.image.url}" width="50">')
        else:
            return '-'

    image_preview.short_description = 'Превью'


class ProductAdminView(admin.ModelAdmin):
    list_display = ['id', 'title', 'preview_about', 'get_short_about',
                    'get_short_features', 'price', 'old_price',
                    'stock', 'created_at', 'category', 'first_image_preview']
    list_display_links = ['id', 'title', 'get_short_about', 'get_short_features', 'price',
                          'old_price', 'stock']
    search_fields = ['title', 'about']
    list_filter = ['category']
    inlines = [ProductTabular]

    def get_short_about(self, obj):
        return obj.about[:150] + '...'

    get_short_about.short_description = 'О товаре'

    def get_short_features(self, obj):
        return obj.features[:150] + '...'

    get_short_features.short_description = 'Характеристики'

    def first_image_preview(self, obj):
        if obj.image.exists():
            return format_html(f'<img src="{obj.image.first().image.url}" width="50">')
        else:
            return '-'

    first_image_preview.short_description = 'Превью'


class ProductImageAdminView(admin.ModelAdmin):
    list_display = ['id', 'image', 'image_preview', 'created_at']
    list_display_links = ['id', 'created_at']
    list_filter = ['created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="30">')
        else:
            return '-'

    image_preview.short_description = 'Превью'


class DiscountAdminView(admin.ModelAdmin):
    list_display = ['id', 'code', 'discount_percentage',
                    'start_date', 'end_date', 'active']
    list_display_links = ['id', 'code']


class QuestionAdminView(admin.ModelAdmin):
    list_display = ['id', 'owner', 'content', 'product',
                    'approved', 'published']
    list_display_links = ['id', 'owner', 'content',
                          'product', 'published']
    list_filter = ['published']
    search_fields = ['content']
    list_editable = ['approved']


class WishlistAdminView(admin.ModelAdmin):
    list_display = ['id', 'owner', 'get_products_list', 'created_at']
    list_display_links = ['id', 'owner']

    def get_products_list(self, obj):
        return format_html('<br>'.join([str(item.id) + ' ' + str(item) for item in obj.products.all()]))
    get_products_list.short_description = 'Товары'


admin.site.register(Product, ProductAdminView)
admin.site.register(ProductImage, ProductImageAdminView)
admin.site.register(Discount, DiscountAdminView)
admin.site.register(Question, QuestionAdminView)
admin.site.register(Wishlist, WishlistAdminView)