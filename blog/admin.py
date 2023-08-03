from django.contrib import admin
from blog.models import Post, Comment, Tag, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'content', 'category', 'image', 'published']
    list_display_links = ['id', 'owner', 'title', 'content', 'category', 'image']
    list_filter = ['owner', 'category', 'published']
    search_fields = ['title', 'content']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'content', 'owner', 'published', 'approved']
    list_display_links = ['id', 'post', 'content', 'owner', 'published']
    list_filter = ['owner', 'published']
    list_editable = ['approved']
    search_fields = ['content']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)