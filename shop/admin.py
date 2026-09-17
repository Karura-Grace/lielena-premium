from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "product_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("order", "name")

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "category",
        "price",
        "in_stock",
        "is_featured",
        "created_at",
    )
    list_display_links = ("thumbnail", "name")
    list_filter = ("category", "in_stock", "is_featured")
    list_editable = ("price", "in_stock", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    readonly_fields = ("preview", "created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "category", "description"),
        }),
        ("Pricing & stock", {
            "fields": ("price", "in_stock", "is_featured"),
        }),
        ("Image", {
            "fields": ("image", "preview"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;'
                'border-radius:6px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:320px;max-height:320px;'
                'object-fit:cover;border-radius:10px;" />',
                obj.image.url,
            )
        return "No image uploaded yet."


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "total", "created_at")
    search_fields = ("first_name", "last_name", "email")
    readonly_fields = (
        "first_name", "last_name", "email", "phone",
        "address", "city", "country", "total", "created_at",
    )
    inlines = (OrderItemInline,)


admin.site.site_header = "LIELENA Admin"
admin.site.site_title = "LIELENA Admin"
admin.site.index_title = "Manage your catalog"
