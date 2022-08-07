from django.contrib import admin

from .models import Category, Product, Bid, SoldProduct


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class BidAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(SoldProduct)
