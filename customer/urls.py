from django.urls import path

from .views import *

urlpatterns = [
    path('', LP.as_view(), name="LP"),
    path('login/', Login.as_view(), name="login"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('logout/', Logout.as_view(), name="logout"),
]