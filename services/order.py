import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: Optional[datetime] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        if date is not None:
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            ms = MovieSession.objects.get(pk=ticket["movie_session"])
            Ticket.objects.create(
                order=order,
                movie_session=ms,
                row=ticket["row"],
                seat=ticket["seat"])
        return order


def get_orders(username: str = None) -> QuerySet[Order]:

    if username is None:
        return Order.objects.all()
    else:
        return Order.objects.filter(
            user__username=username).select_related("user").order_by("-created_at")
