from django.contrib import admin

from catalog.models import Categories
from products.models import Product, ImageForProduct, SpecificationsForProduct
from tags.models import Tags
from orders.models import Order, ProductsInOrder, Delivery, Payment


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'parent']
    list_display_links = ['title']
    ordering = ['title']
    search_fields = ['title']


class ImageAdminInline(admin.StackedInline):
    model = ImageForProduct


class SpecificationsAdminInline(admin.StackedInline):
    model = SpecificationsForProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageAdminInline,
        SpecificationsAdminInline,
    ]
    list_display = ['pk', 'category', 'title', 'price', 'description', 'freeDelivery', 'limitedEdition', 'onSales']
    list_display_links = ['title', 'description']
    ordering = ['category', 'title', 'price']
    search_fields = ['title', 'description']


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['type']
    list_display_links = ['type']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['type', 'freePrice', 'tax']
    list_display_links = ['type']


class OrderProductAdminInline(admin.StackedInline):
    model = ProductsInOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductAdminInline,
    ]
    list_display = ['pk', 'fullName', 'deliveryType', 'paymentType',
                    'totalCost', 'status', 'city', 'address']
    list_display_links = ['pk', 'fullName', 'status']
    ordering = ['status']
    search_fields = ['status', 'city', 'address']

