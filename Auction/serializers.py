from rest_framework import serializers
from .models import Category, Product, Bid
from django.core.exceptions import ValidationError
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = instance.category.name
        response['user'] = instance.user.username

        return response


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

    def validate(self, data):
        last_bid = Bid.objects.filter(product=data.get('product').id, user=data.get('user')).last()
        if last_bid:
            diff = int((timezone.now() - last_bid.time).total_seconds())
            if diff < 10:
                raise ValidationError({"time": "ბოლო შეთავაზებიდან 10 წამი არ გასულა"})

        if data.get('price'):
            if data.get('product').current_price > data.get('price'):
                raise ValidationError({"price_error": "შენი შეთავაზება მიმდინარე ფასზე მეტი უნდა იყოს"})

        return data