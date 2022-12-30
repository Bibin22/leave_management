from django.db import models
import uuid
from django.contrib.auth.models import User


class LeaveApplication(models.Model):
    leave_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_user = models.CharField(max_length=50, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_user = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    leave_type = models.ForeignKey('admin_app.LeaveType', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_days = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.leave_type

