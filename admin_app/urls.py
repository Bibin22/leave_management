from django.urls import path
from .views import *

urlpatterns = [
    path('holiday_add',HolidayAdd.as_view(), name='holiday_add'),
    path('leaves',Leaves.as_view(), name='leaves'),
    path('leave_applications_list/',LeaveApplicationList.as_view(), name='leave_applications_list'),
    path('leave_review/<str:id>',LeaveApplicationReview.as_view(), name='leave_review'),
    path('employee_list', EmployeeList.as_view(), name='employee_list'),
    path('monthly_report/<str:id>',MonthlyReport.as_view(), name='monthly_report'),

]