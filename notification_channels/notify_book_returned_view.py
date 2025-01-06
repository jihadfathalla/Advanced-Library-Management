from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.translation import gettext as _


def notify_book_returned(book_title, branch_name):
    channel_layer = get_channel_layer()
    message = _(
        (f"The book '{book_title}' is now available now in this branch {branch_name}.")
    )
    async_to_sync(channel_layer.group_send)(
        "books_notifications",
        {
            "type": "send_book_notification",
            "message": message,
        },
    )


def test_notify_book_returned(request):
    ## daphne -p 8000 config.asgi:application
    return render(request, "index.html")
