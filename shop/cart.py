from decimal import Decimal, ROUND_DOWN
from django.conf import settings
from .models import Product, Discount


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.setdefault(settings.CART_SESSION_ID, {})
        self.cart = cart
        self.discount_id = self.session.get('discount', None)

    def setter(self, data):
        self.cart = self.session[settings.CART_SESSION_ID] = data

    def add(self, product, quantity=1, update=False):
        """
        Добавляет товар в корзину/Обновляет количество товара в корзине
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += 1

        self.save()

    def save(self):
        """
        Сохраняет корзину в сессии
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def __iter__(self):
        """
        Итератор товаров к корзине
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * int(item['quantity'])
            yield item

    def __len__(self):
        """
        Получить количество всех товаров в корзине
        """
        return len(self.cart.items())

    def get_total_price(self):
        """
        Получить стоимость всех товаров в корзине
        """
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())

    def get_item_total_price(self, id: int) -> Decimal:
        return Decimal(self.cart[str(id)]['price'])*int(self.cart[str(id)]['quantity'])

    def clean(self):
        """
        Полностью удаляет корзину
        """
        if self.session.get('discount', None):
            del self.session['discount']
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def list_items(self):
        """
        Возвращает список id товаров в корзине
        """
        return [int(id) for id in self.cart.keys()]

    def merge_session_cart(self):
        pass

    @property
    def coupon(self):
        if self.discount_id:
            return Discount.objects.get(id=self.discount_id)
        else:
            return None

    def get_discount(self):
        if self.coupon:
            return self.get_total_price() * (Decimal(self.coupon.discount_percentage)/100)
        else:
            return Decimal('0')

    def get_the_final_total_price(self):
        return round(self.get_total_price() - self.get_discount(), 2)