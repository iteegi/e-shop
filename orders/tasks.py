"""Task."""

from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    """Send an email notification when placing an order successfully."""
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Дорогой {},\n\n Вы успешно разместили заказ.\
    Ваш идентификатор заказа {}.'.format(order.first_name, order.id)

    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
