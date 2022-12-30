from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *

urlpatterns = [
    path('login',obtain_auth_token, name='login'),
    path('logout',LogOut.as_view(), name='logout'),
    path('registration',UserRegistration.as_view(), name='registration'),
    path('edit_employee/<str:id>',EditEmployee.as_view(), name='edit_employee'),
]