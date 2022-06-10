from django.urls import path
from .views import CategoryView, ProductView, BidView

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('product/', ProductView.as_view(), name='products'),
    path('bids/', BidView.as_view(), name='bid'),

]
