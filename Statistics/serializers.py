from rest_framework import serializers
from Auction.models import Product, Bid
from django.db.models import Count


class ProductStatSerializer(serializers.ModelSerializer):
    bid_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_bid_count(self, obj):
        product = Product.objects.filter(id=obj.id).annotate(count=Count('bid'))
        bid = list(Bid.objects.filter(product=product[0].id).values())
        data = {"count": product[0].count, "bid": list(bid)}
        return data
