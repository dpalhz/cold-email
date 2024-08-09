import uuid
from django.db import models
from ckeditor.fields import RichTextField
from authentication.models import CustomUser
from email_data.models import Department

class EmailSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_schedules')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='email_schedules')
    subject = models.CharField(max_length=255, null=True)
    content = RichTextField(blank=True, null=True) 
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_sent = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.subject} - {self.user.email}"