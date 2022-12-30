from django.urls import path
from .views import *

urlpatterns = [
    path('leave_request',LeaveRequest.as_view(), name='leave_request'),
]