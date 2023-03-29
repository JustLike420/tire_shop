from django.contrib import admin

from .models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class OrderAdmin(admin.ModelAdmin):
    pass


class OrderItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
