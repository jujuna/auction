from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('სახელი'))

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('სახელი'))
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('კატეგორია'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    starting_price = models.IntegerField(verbose_name=_('საწყისი ფასი'))
    preferred_price = models.IntegerField(verbose_name=_('სასურველი ფასი'))
    current_price = models.IntegerField(verbose_name=_('მიმდინარე ფასი'), default=0)
    send_to_email = models.BooleanField()
    time = models.DateTimeField(auto_now=True, verbose_name=_('დრო'))
    sold = models.BooleanField(default=False)
    sold_time = models.DateTimeField(null=True, blank=True,)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.current_price == 0:
            self.current_price = self.starting_price
        super(Product, self).save(*args, **kwargs)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('პროდუქტი'))
    price = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('დრო'))
    time.editable = True
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + ' -> ' + str(self.price)

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.product.current_price += 1
            self.product.save()
            self.price = self.product.current_price
        else:
            self.product.current_price += self.price - self.product.current_price
            self.product.save()

        super(Bid, self).save(*args, **kwargs)


class SoldProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('პროდუქტი'))
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('ბიდი'))
    time = models.DateTimeField(auto_now=True, verbose_name=_('დრო'))

    def __str__(self):
        return f'{self.product} - > ფასი - > {self.bid.price}'
