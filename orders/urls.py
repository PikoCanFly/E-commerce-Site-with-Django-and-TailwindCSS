from django.urls import path
from .views import order_create, order_confirmation

app_name = "orders"

urlpatterns = [
    path('create', order_create, name="order_create"),
    path("confirmation/<int:order_id>", order_confirmation, name="order_confirmation"),
]
