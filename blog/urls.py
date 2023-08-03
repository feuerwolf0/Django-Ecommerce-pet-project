from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('like/', views.like_post, name='like'),
    path('post/<int:id>', views.post_view, name='post'),
    path('category/<slug:slug>', views.by_category_view, name='category'),
    path('tag/<slug:slug>', views.by_tag_view, name='tag'),
    path('tags/', views.all_tags_view, name='tags'),
    path('categories/', views.all_categories_view, name='categories'),
]