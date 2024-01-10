import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction

from blog.models import Category
from order.models import Order, OrderItem
from order.tasks import order_created
from shop.cart import Cart
from users.models import Address


@login_required
def create_order_view(request):
    categories = Category.objects.all()
    # Получаю основной адрес пользователя
    address = Address.objects.filter(user=request.user.profile, is_main=True).first()
    if address:
        cart = Cart(request)

        context = {
            'categories': categories,
            'cart': cart,
            'address': address
        }

        if request.method == 'POST' and cart:

            # Создаю уникальный id товара вида 000-000-000
            order_number = str(random.randint(100, 999)) + '-' + str(random.randint(100, 999)) + '-' + str(random.randint(100, 999))
            while Order.objects.filter(unique_id=order_number).exists():
                order_number = str(random.randint(100, 999)) + '-' + str(random.randint(100, 999)) + '-' + str(random.randint(100, 999))

            if cart.coupon:
                discount = cart.coupon.discount_percentage
            else:
                discount = 0

            # Если в процессе создания заказа возникнут ошибки, создание заказа будет отменено
            with transaction.atomic():
                new_order = Order.objects.create(
                    owner=request.user.profile,
                    full_name=address.full_name,
                    phone_number=address.phone_number,
                    address=address.get_full_address(),
                    total_price=cart.get_total_price(),
                    end_price=cart.get_the_final_total_price(),
                    discount_percent=discount,
                    unique_id=order_number
                )
                # Добавляю товары из корзины в заказ
                for item in cart:

                    product_obj = item['product']
                    product_obj.stock -= int(item['quantity'])
                    product_obj.save()

                    OrderItem.objects.create(order=new_order,
                                             product=item['product'],
                                             unit_price=item['price'],
                                             quantity=item['quantity'])
                # Отправляю письмо на почту
                order_created.delay(order_number)

                cart.clean()

                return redirect('order:order_detail', order_id=order_number)

        return render(request, 'create_order.html', context)
    else:
        messages.success(request, 'У вас не указан основной адрес. Выберите основной адрес или добавьте новый')
        return redirect('users:addresses')


@login_required
def order_detail_view(request, order_id):
    categories = Category.objects.all()
    # Получаю заказ по профилю и уникальному id заказа
    order = Order.objects.filter(owner=request.user.profile, unique_id=order_id).first()

    if order:

        context = {
            'categories': categories,
            'order': order
        }

        # Если нажата кнопка оплаты
        if request.method == 'POST':
            # Изменяю статус заказа на оплачено
            order.paid = True
            order.save()
            # Перезагружаю страницу
            return redirect('.')

        return render(request, 'order_detail.html', context)

    else:
        return redirect('store:cart_view')


@login_required
def my_orders_view(request):
    categories = Category.objects.all()
    # Получаю все заказы пользователя
    orders = Order.objects.filter(owner=request.user.profile)
    # Получаю все оплаченные заказы пользователя
    paid_orders = orders.filter(paid=True)
    # Получаю не оплаченные заказы
    unpaid_orders = orders.filter(paid=False)

    context = {
        'categories': categories,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders
    }
    return render(request, 'orders.html', context)