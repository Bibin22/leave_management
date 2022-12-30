from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from user_app.models import *


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = ['holiday_name', 'holiday_date']



class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['leave_type']

class LeaveApplicationRequest(serializers.ModelSerializer):
    leave_types = serializers.CharField(source='leave_type.leave_type')
    users = serializers.CharField(source='user.username')
    class Meta:
        model = LeaveApplication
        fields = ['leave_id','leave_types', 'users', 'start_date', 'end_date', 'total_days', 'reason', 'status']


class LeaveApplicationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['status']


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email']


class DateFilter(serializers.Serializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField()