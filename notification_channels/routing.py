from django.urls import path
from notification_channels import consumers

websocket_urlpatterns = [
    path("ws/books/", consumers.BookNotificationConsumer.as_asgi()),
]
