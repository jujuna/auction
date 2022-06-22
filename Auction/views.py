from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, BidSerializer
from .models import Category, Product, Bid
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound


User = get_user_model()


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = Product.objects.filter(sold=False)
        return queryset


class BidView(generics.ListCreateAPIView):
    serializer_class = BidSerializer
    queryset = Bid.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_email = Product.objects.get(id=request.data['product']).send_to_email
        if send_email:
            product = Product.objects.filter(id=request.data['product'], user=self.request.user).last()
            user = User.objects.get(id=request.data['user']).username
            subject = 'ბიდი'
            message = f'შემოთავაზება {user}-სგან {product}-ზე. ფასი {product.current_price} ლარი'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["zhuzhunadze1@gmail.com", ]
            send_mail(subject, message, email_from, recipient_list)

        return Response(serializer.data)


class BidAccept(generics.CreateAPIView):

    def send_email_to_buyer(self, product, price, email):
        subject = f'გილოცავ! შენ მოიგე {product}'
        message = f'{product} შენია {price} ლარად.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

    def get_object(self):
        try:
            return Bid.objects.get(id=self.kwargs['pk'])
        except Bid.DoesNotExist:
            raise NotFound(detail="ბიდი ვერ მოიძებნა")

    def post(self, request, *args, **kwargs):
        bid = self.get_object()
        product = Product.objects.get(id=request.data['product'])
        if self.request.user == product.user:
            bid.accept = True
            product.sold = True
            bid.save()
            product.save()
            self.send_email_to_buyer(product.name, bid.price, bid.user.email)

        return Response({"created"})
