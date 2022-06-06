from django.contrib import admin

from .models import Category, Product, Bid

admin.site.register([Category, Product, Bid])
