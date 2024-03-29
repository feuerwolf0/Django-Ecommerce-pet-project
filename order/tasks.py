from django.core.mail import send_mail, get_connection
from .models import Order
from django.conf import settings
from django.shortcuts import reverse
from config.celery import app


@app.task()
def order_created(order_id):
    order = Order.objects.get(unique_id=order_id)
    subject = f'Заказ №{order_id} создан'
    message = f'Уважаемый {order.full_name}, \n \
                Вы оформили заказ на нашем сайте.\n \
                Ваш номер заказа {order_id}. \n \
                Ваш заказ доступен по ссылке {settings.BASE_URL}{reverse("order:order_detail", args=[order_id])}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = [order.owner.email]
    mail_sent = send_mail(subject, message, from_email, recipient)
    return mail_sent
