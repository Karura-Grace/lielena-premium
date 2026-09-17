import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem


def home(request):
    featured = Product.objects.filter(is_featured=True, in_stock=True).select_related("category")[:8]
    if not featured.exists():
        # Nothing marked as featured yet — just show the newest items so the
        # homepage never looks empty.
        featured = Product.objects.filter(in_stock=True).select_related("category")[:8]
    categories = Category.objects.all()
    return render(request, "shop/home.html", {
        "featured_products": featured,
        "categories": categories,
    })


def shop(request):
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    active_category = request.GET.get("category", "").strip()
    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)

    return render(request, "shop/shop.html", {
        "products": products,
        "categories": categories,
        "active_category": active_category,
        "query": query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related = (
        Product.objects.filter(category=product.category, in_stock=True)
        .exclude(pk=product.pk)
        .select_related("category")[:4]
    )
    return render(request, "shop/product_detail.html", {
        "product": product,
        "related_products": related,
    })


def checkout(request):
    return render(request, "shop/checkout.html")


@require_POST
def place_order(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse({"error": "That request didn't look right."}, status=400)

    items = data.get("items") or []
    if not items:
        return JsonResponse({"error": "Your cart is empty."}, status=400)

    first_name = (data.get("first_name") or "").strip()
    email = (data.get("email") or "").strip()
    if not first_name or not email:
        return JsonResponse({"error": "Name and email are required."}, status=400)

    order = Order.objects.create(
        first_name=first_name,
        last_name=(data.get("last_name") or "").strip(),
        email=email,
        phone=(data.get("phone") or "").strip(),
        address=(data.get("address") or "").strip(),
        city=(data.get("city") or "").strip(),
        country=(data.get("country") or "").strip(),
    )

    total = 0
    for item in items:
        try:
            price = float(item.get("price", 0))
            qty = int(item.get("qty", 1))
        except (TypeError, ValueError):
            continue
        if qty <= 0:
            continue
        product = Product.objects.filter(slug=item.get("id")).first()
        OrderItem.objects.create(
            order=order,
            product=product,
            name=item.get("name") or (product.name if product else "Item"),
            price=price,
            quantity=qty,
        )
        total += price * qty

    order.total = total
    order.save(update_fields=["total"])

    return JsonResponse({"order_id": order.pk})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "shop/order_confirmation.html", {"order": order})
