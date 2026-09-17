from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/place-order/", views.place_order, name="place_order"),
    path("order/<int:order_id>/confirmation/", views.order_confirmation, name="order_confirmation"),
]
