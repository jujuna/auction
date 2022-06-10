from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, BidSerializer
from .models import Category, Product, Bid
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BidView(generics.ListCreateAPIView):
    serializer_class = BidSerializer
    queryset = Bid.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # product = Product.objects.get(id=request.data['product'])
        # user = User.objects.get(id=request.data['user']).username
        # subject = 'ბიდი'
        # message = f'შემოთავაზება {user}-სგან {product}-ზე. ფასი {request.data["price"]} ლარი'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ["zhuzhunadze1@gmail.com", ]
        # send_mail(subject, message, email_from, recipient_list)

        return Response(serializer.data)





