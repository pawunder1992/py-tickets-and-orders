import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: dict,
        username: str,
        date: datetime.datetime = None) -> None:
    order = Order.objects.create(user=get_user_model()
                                 .objects.get_or_create(username=username)[0])
    if date:
        order.created_at = date
    order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    # list_of_tickets = []
    # Ticket.objects.bulk_create([Ticket(movie_session_id=ticket["movie_session"],
    #         order=order,
    #         row=ticket["row"],
    #         seat=ticket["seat"]) for ticket in tickets])
    # Not work with atomic test


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
