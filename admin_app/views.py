from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .paginations import *
from user_app.models import *
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Sum


class HolidayAdd(APIView):
    permission_classes = [IsAuthenticated]
    serializers_class = HolidaySerializer

    def get(self, request):
        try:
            # pagination_class = HolidayPagination
            holidays = Holidays.objects.all()
            serializer = HolidaySerializer(holidays, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:

            result = {
                "msg":"something went wrong"
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if request.user.is_superuser:
                serializer = HolidaySerializer(data=request.data)
                print(request.data)
                if serializer.is_valid():
                    serializer.validated_data['created_user'] = request.user
                    serializer.save()
                    return Response(request.data, status=status.HTTP_201_CREATED)
                else:
                    data = serializer.errors
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                results = {
                    "msg":"only superuser can add holidays "
                }
                return Response(results, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)




class Leaves(APIView):
    permission_classes = [IsAuthenticated]
    serializers_class = LeaveSerializer

    def get(self, request):
        try:
            leaves = LeaveType.objects.all()
            serializer = LeaveSerializer(leaves, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            results = {
                "msg":"something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = LeaveSerializer(data=request.data)
            print(request.data)
            if request.user.is_superuser:
                if serializer.is_valid():
                    serializer.validated_data['created_user'] = request.user
                    serializer.save()
                    return Response(request.data, status=status.HTTP_201_CREATED)
                else:
                    data = serializer.errors
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                results = {
                    "msg":"only superuser can add leave "
                }
                return Response(results, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)




class LeaveApplicationList(APIView):
    permission_classes = [IsAuthenticated]
    serializers_class = LeaveApplicationRequest

    def get(self, request):
        try:
            if request.user.is_superuser:
                leaves = LeaveApplication.objects.all()
                serializer = LeaveApplicationRequest(leaves, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                result = {
                    "msg":"only super user can view this list"
                }
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except:
            result = {
                "msg":"something went wrong"
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)



# class LeaveApplicationList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = LeaveApplication.objects.all()
#     serializer_class = LeaveApplicationRequest


class LeaveApplicationReview(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveApplicationReviewSerializer

    def get(self, request, id):
        try:
            if request.user.is_superuser:
                leave = LeaveApplication.objects.get(leave_id=id)
                results = {
                    "user": leave.user.username,
                    "reason": leave.reason,
                    "start_date": leave.start_date,
                    "end_date": leave.end_date,

                }
                return Response(results, status=status.HTTP_200_OK)
            else:
                result = {
                    "msg":"only superuser can approve leave"
                }
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        except:
            results = {
                "msg":"something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            if request.user.is_superuser:
                leave = LeaveApplication.objects.get(leave_id=id)
                serializer = LeaveApplicationReviewSerializer(leave, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    data = serializer.errors
                    return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                result = {
                    "msg": "only superuser can approve leave"
                }
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)



class EmployeeList(APIView):
    def get(self, request):
        try:
            if request.user.is_superuser:
                user = User.objects.all()
                serializer = EmployeeListSerializer(user, many=True)
                return Response(serializer.data)
            else:
                result = {
                    "msg": "only superuser can see employees"
                }
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)


class MonthlyReport(APIView):
    serializer_class = DateFilter
    permission_classes = [IsAuthenticated]
    def post(self, request,id, format=None):
        try:
            if request.user.is_superuser:
                serializer = DateFilter(data=request.data)

                if serializer.is_valid():
                    start_date = serializer.validated_data.get("start_date")
                    end_date = serializer.validated_data.get("end_date")
                    start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
                    end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
                    end_date = end_date + timedelta(days=1)

                    response = HttpResponse(content_type='application/ms-excel')
                    file_name = "report.csv"
                    response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'
                    writer = csv.writer(response)
                    user = User.objects.get(id=id)
                    writer.writerow(
                        ["Employee :" f"{user.first_name} {user.last_name} ", f"From Date : {start_date}",
                         f"To Date:  {end_date}", ])
                    writer.writerow([""])
                    leave_applied = LeaveApplication.objects.filter(start_date__range=[start_date, end_date], user__id=id)
                    total_applied = leave_applied.count()
                    approved = leave_applied.filter(status="Approved").count()
                    rejected = leave_applied.filter(status="Rejected").count()
                    pending = leave_applied.filter(status="Pending").count()
                    total_leaves = leave_applied.filter(status="Approved").aggregate(Sum('total_days'))
                    total_leaves = total_leaves['total_days__sum']
                    writer.writerow([""])
                    writer.writerow(
                        [f"Total Leave Applied : {total_applied}", f"Approved: {approved}", f"Rejected : {rejected}",
                         f"Pending: {pending}", f"Total Approved Leaves: {total_leaves}"])
                    writer.writerow([""])
                    writer.writerow([""])
                    first_row = ["Start Date", "End Date", "Total Days ", "Reason", "Status"]
                    writer.writerow(first_row)
                    for i in leave_applied:
                        second_row = [i.start_date, i.end_date, i.total_days, i.reason, i.status]
                        writer.writerow(second_row)
                    return response
                else:
                    data = serializer.errors
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = {
                    "msg": "only superuser can see download reports"
                }
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        except:
            results = {
                "msg": "something went wrong"
            }
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

