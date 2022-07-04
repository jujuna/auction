from django.urls import path
from .views import MyProducts, MaxBids, LastSold, TopActiveUser, RecommendedProduct

urlpatterns = [
    path('my-products/', MyProducts.as_view(), name="my-products"),
    path('max-bid/', MaxBids.as_view(), name="max-bid"),
    path('last-sold/', LastSold.as_view(), name="last-sold"),
    path('top-user/', TopActiveUser.as_view(), name="top-user"),
    path('recommended/', RecommendedProduct.as_view(), name="recommended"),
]