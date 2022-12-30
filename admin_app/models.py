from django.db import models

# Create your models here.
import uuid

class Holidays(models.Model):
    holiday_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_user = models.CharField(max_length=50, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_user = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    holiday_name = models.CharField(max_length=50, null=True, blank=True)
    holiday_date = models.DateField(null=True, blank=True)


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.holiday_name)


class LeaveType(models.Model):
    leave_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_user = models.CharField(max_length=50, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_user = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    leave_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.leave_type)
