from django.urls import path
from .views import Registration, Login
urlpatterns = [
    path('reg/', Registration.as_view(), name='registration'),
    path('log/', Login.as_view(), name='login'),
]
