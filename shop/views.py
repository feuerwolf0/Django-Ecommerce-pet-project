from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.utils import timezone

from blog.models import Category, Tag
from .models import Product, Wishlist, Discount
from .cart import Cart


def handle_filters(request, products):
    """
    Применяет фильтры к товарам и возвращает отфильтрованный queryset товаров
    """
    sort_options = {
        '': '-created_at',
        'date_desc': 'created_at',
        'price_asc': 'price',
        'price_desc': '-price'
    }
    sort_by = request.GET.get('sort_by', '')
    products = products.order_by(sort_options.get(sort_by, '-created_at'))

    show_options = {
        '': 10,
        '25': 25,
        '50': 50
    }
    show_by = request.GET.get('show_by', '')
    if show_by != 'all':
        products = products[:show_options.get(show_by, 10)]

    return sort_by, show_by, products


def shop_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    last_products = products[:3]
    wishlist = None

    # Если пользователь аноним
    if request.user.id:
        wishlist = Wishlist.objects.filter(owner__id=request.user.profile.id).first()

    # Применяю фильтры
    sort_by, show_by, products = handle_filters(request, products)

    cart = Cart(request)

    context = {
        'categories': categories,
        'last_products': last_products,
        'sort_by': sort_by,
        'show_by': show_by,
        'products': products,
        'wishlist': wishlist,
        'cart': cart,
    }
    return render(request, 'shop.html', context)


def category_view(request, slug):
    categories = Category.objects.all()
    last_products = Product.objects.all()[:3]
    wishlist = None

    # Если пользователь не аноним получаю wishlist из бд
    if request.user.id:
        wishlist = Wishlist.objects.filter(owner__id=request.user.profile.id).first()

    products = Product.objects.filter(category__slug=slug)
    current_category = Category.objects.get(slug=slug)

    sort_by, show_by, products = handle_filters(request, products)

    context = {
        'categories': categories,
        'last_products': last_products,
        'current_category': current_category,
        'sort_by': sort_by,
        'show_by': show_by,
        'products': products,
        'wishlist': wishlist
    }
    return render(request, 'shop_by_category.html', context)


def tag_view(request, slug):
    categories = Category.objects.all()
    wishlist = None

    # Если пользователь не аноним получаю wishlist из бд
    if request.user.id:
        wishlist = Wishlist.objects.filter(owner__id=request.user.profile.id).first()

    last_products = Product.objects.all()[:3]
    products = Product.objects.filter(tags__slug=slug)
    current_tag = Tag.objects.get(slug=slug)

    sort_by, show_by, products = handle_filters(request, products)

    context = {
        'categories': categories,
        'last_products': last_products,
        'current_tag': current_tag,
        'sort_by': sort_by,
        'show_by': show_by,
        'products': products,
        'wishlist': wishlist
    }

    return render(request, 'shop_by_tag.html', context)


@login_required
def add_wishlist(request):
    pid = request.GET.get('product')
    product = get_object_or_404(Product, id=pid)
    data = {}
    check_wishlist = Wishlist.objects.filter(products=product, owner__id=request.user.profile.id).count()
    if check_wishlist > 0:
        wishlist = get_object_or_404(Wishlist, owner=request.user.profile)
        wishlist.products.remove(product)
        data = {
            'bool': False
        }
    else:
        wishlist, created = Wishlist.objects.get_or_create(owner=request.user.profile)
        wishlist.products.add(product)
        data = {
            'bool': True
        }
    return JsonResponse(data)


@login_required
def wishlist_view(request):
    categories = Category.objects.all()
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user.profile)

    if request.method == 'POST':
        if request.POST.get('item_id'):
            product_id = int(request.POST.get('item_id'))
            product = Product.objects.get(id=product_id)
            if request.user.profile == wishlist.owner:
                wishlist.products.remove(product)
        else:
            wishlist.products.clear()

    cart = Cart(request)

    context = {
        'categories': categories,
        'wishlist': wishlist,
        'cart': cart
    }
    return render(request, 'wishlist.html', context)


def shop_detail_view(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    # 5 последних новинок
    last_products = Product.objects.all()[:5]

    wishlist = None
    if request.user.id:
        wishlist = Wishlist.objects.filter(owner__id=request.user.profile.id).first()

    cart = Cart(request)

    context = {
        'product': product,
        'categories': categories,
        'last_products': last_products,
        'cart': cart,
        'wishlist': wishlist
    }
    return render(request, 'shop_detail.html', context)


def cart_add(request):
    """
    Добавляет товар в корзину
    """
    # Получаю id товара, количетсво и update для корзины
    pid: int = request.GET.get('product_id')
    quantity: int = request.GET.get('quantity')
    update: bool = bool(int(request.GET.get('update')))

    product = get_object_or_404(Product, id=pid)
    cart = Cart(request)
    cart.add(product, quantity, update)

    return JsonResponse({'bool': True})


def cart_view(request):
    categories = Category.objects.all()
    cart = Cart(request)
    context = {
        'categories': categories,
        'cart': cart
    }
    return render(request, 'cart.html', context)


def update_cart(request):
    pid = request.GET.get('product_id')
    quantity = request.GET.get('quantity')
    update = bool(int(request.GET.get('update')))

    product = get_object_or_404(Product, id=pid)
    cart = Cart(request)
    # Добавляю товар в корзину
    cart.add(product, quantity, update)
    item_total_price = cart.get_item_total_price(pid)
    total_price = cart.get_the_final_total_price()
    discount = round(cart.get_discount(), 2)
    return JsonResponse({'itotal': item_total_price, 'total': total_price, 'discount': discount})


@require_POST
def remove_cart(request, pid):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pid)
    cart.remove(product)
    messages.success(request, f'Товар { product.title } удален из корзины')
    return HttpResponseRedirect(reverse_lazy('store:cart_view'))


@require_POST
def clean_cart(request):
    cart = Cart(request)
    cart.clean()
    messages.success(request, 'Корзина очищена')
    return redirect('store:cart_view')


@require_POST
def apply_discount(request):
    # Получаю промокод
    promocode = request.POST.get('promocode', None)
    # Получаю время
    time_now = timezone.now()
    try:
        discount = Discount.objects.get(code__iexact=promocode,
                                        start_date__lte=time_now,
                                        end_date__gte=time_now,
                                        active=True)
        request.session['discount'] = discount.id
        messages.info(request, f'Купон { promocode } применён!', extra_tags='discount')

    except Discount.DoesNotExist:
        request.session['discount'] = None
        messages.info(request, f'Купон { promocode } не сущетвует!', extra_tags='invalid')

    return redirect('store:cart_view')
