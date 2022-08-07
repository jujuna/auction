import json
from rest_framework import generics
from rest_framework.response import Response
from Auction.models import Product, Bid, Category
from Auction.serializers import BidSerializer, ProductSerializer
from .serializers import ProductStatSerializer
from rest_framework.views import APIView
import datetime
from django.forms.models import model_to_dict
from django.db.models import Count, Max
from django.contrib.auth import get_user_model
from collections import Counter
import random


User = get_user_model()


class MyProducts(generics.ListAPIView):
    serializer_class = ProductStatSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        return queryset


class MaxBids(APIView):

    def get(self, request):
        week = datetime.date.today() - datetime.timedelta(days=7)
        day = datetime.date.today() - datetime.timedelta(days=1)

        max_bid_by_week = Bid.objects.filter(time__gte=week).order_by('price').last()
        max_bid_by_day = Bid.objects.filter(time__gte=day).order_by('price').last()

        json_data = {'max_bid_by_week': model_to_dict(max_bid_by_week), 'max_bid_by_day': model_to_dict(max_bid_by_day)}

        return Response(json_data)


class LastSold(APIView):

    def get(self, request):
        data = Product.objects.filter(sold=True).order_by('sold_time').values()
        return Response(data)


class TopActiveUser(APIView):

    def get(self, request):
        data = User.objects.values('id').annotate(count=Count('bid')).order_by('-count')[0:3]
        return Response({"data": data})


class RecommendedProduct(APIView):

    def statistic(self):
        data = []
        all_products = list(Product.objects.filter(user=self.request.user).values('category'))
        products_id = [data.append(all_products[i]['category']) for i in range(len(all_products))]
        all_bids = list(Bid.objects.filter(user=self.request.user).values('product__category'))
        bids_id = [data.append(all_bids[i]['product__category']) for i in range(len(all_bids))]
        most_common = Counter(data).most_common()
        full_data = {"number_list": data, "common": [i[0] for i in most_common[0:int(len(most_common)/2+1)]]}
        return full_data

    def get(self, request):
        stats = self.statistic()

        if len(stats['number_list']) >= 10:
            data = Product.objects.all().filter(category_id__in=stats['common']).values()
            return Response({"data": data})
        else:
            return Response({"count_len": "მონაცემის ანალიზისთვის არ არის საკმარისი რაოდენობა"})
