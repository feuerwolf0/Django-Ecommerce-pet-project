from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

from .models import Post, Tag, Category, Comment
from .utils import paginate
from shop.models import Product


def base_data():
    """
    Возвращает объекты последних комментариев,
    категорий и тэгов для главной страницы
    """
    tags = Tag.objects.annotate(num_posts=Count('posts'), num_prod=Count('tags_products'))
    # Добавляю аннотацию total для количества постов и продуктов с каждым тегом
    tags = tags.annotate(total=F('num_posts')+F('num_prod')).order_by('-total')[:5]
    # Получаю 5 последних комментариев подтвежденных модератором
    comments = Comment.objects.filter(approved=True)[:5]
    # Получаю все категории
    categories = Category.objects.all()
    return tags, comments, categories


def index_view(request):
    tags, comments, categories = base_data()
    posts, custom_range = paginate(request, Post.objects.all(), settings.PER_PAGE)
    context = {'posts': posts,
               'tags': tags,
               'categories': categories,
               'comments': comments,
               'custom_range': custom_range}
    return render(request, 'index.html', context)


def by_category_view(request, slug):
    posts = Post.objects.filter(category_id__slug=slug)
    products = Product.objects.filter(category__slug=slug)
    cat_name = Category.objects.get(slug=slug).name
    tags, comments, categories = base_data()
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'comments': comments,
        'cat_name': cat_name,
        'products': products
    }
    return render(request, 'by_category.html', context)


def by_tag_view(request, slug):
    posts = Post.objects.filter(tags__slug=slug)
    tag_name = Tag.objects.get(slug=slug).name
    tags, comments, categories = base_data()
    products = Product.objects.filter(tags__slug=slug)
    context = {
        'products': products,
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'comments': comments,
        'tag_name': tag_name
    }
    return render(request, 'by_tag.html', context)


def post_view(request, id):
    post = Post.objects.get(pk=id)
    tags, comments, categories = base_data()
    post_comments = post.comments.filter(approved=True)
    form = CommentForm()

    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'comments': comments,
        'post_comments': post_comments,
        'form': form
    }

    if request.method == 'POST':
        if 'content' in request.POST:
            form = CommentForm(request.POST)
            comment = form.save(commit=False)
            comment.post = post
            comment.owner = request.user.profile
            comment.save()
            messages.success(request, 'Ваш комментарий появится после проверки модератором')
            return redirect('blog:post', id=post.id)

        if 'comment_id' in request.POST:
            comment_id = int(request.POST['comment_id'])
            comment = Comment.objects.get(id=comment_id)
            if request.user.is_superuser or request.user == comment.owner:
                comment.delete()
                messages.success(request, 'Комментарий удален')
            else:
                messages.error(request, 'У Вас недостаточно прав на удаление этого комментария')
    return render(request, 'post.html', context)


def all_tags_view(request):
    _, comments, categories = base_data()
    tags = Tag.objects.annotate(num_posts=Count('posts'), num_products=Count('tags_products'))
    tags = tags.annotate(total=F('num_posts') + F('num_products')).order_by('-total')
    context = {
        'tags': tags,
        'categories': categories,
        'comments': comments
    }
    return render(request, 'all_tags.html', context)


def all_categories_view(request):
    # Получаю категории и количество постов и продуктов в них
    categories = Category.objects.annotate(num_cat=Count('post_category'), num_products=Count('category_products'))
    categories = categories.annotate(total=F('num_cat')+F('num_products')).order_by('-total')
    tags, comments, _ = base_data()
    context = {
        'categories': categories,
        'comments': comments,
        'tags': tags
    }
    return render(request, 'all_categories.html', context)


@login_required
def like_post(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    data = {}
    if not post.likes.filter(id=request.user.profile.id).exists():
        post.likes.add(request.user.profile)
        post.save()
        data = {
            'bool': True
        }
    else:
        post.likes.remove(request.user.profile)
        post.save()
        data = {
            'bool': False
        }
    return JsonResponse(data)