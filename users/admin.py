from django.contrib import admin
from django.utils.html import format_html

from users.models import Profile, Address


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'first_name',
                    'last_name',
                    'surname',
                    'email',
                    'created_at',
                    'get_preview_avatar',
                    'avatar',
                    'gender'
                    ]
    list_display_links = ['id',
                          'first_name',
                          'last_name',
                          'surname',
                          'email',
                          'created_at'
                          ]

    def get_preview_avatar(self, obj):
        """
        Отрисовывает изображение картинкой
        """
        return format_html(f'<img src="{obj.avatar.url}" width=50px>')
    get_preview_avatar.short_description = 'Превью'


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user' , 'name', 'full_name', 'phone_number', 'address_line', 'city',
                    'postal_code', 'region', 'country', 'is_main']
    list_display_links = ['id','name', 'full_name', 'phone_number', 'address_line', 'city',
                    'postal_code', 'region', 'country']


admin.site.register(Address, AddressAdmin)
admin.site.register(Profile, ProfileAdmin)