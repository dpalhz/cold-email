import uuid
from django.db import models
from email_data.models import EmailData
from ckeditor.fields import RichTextField
from authentication.models import CustomUser 

class EmailSchedule(models.Model):
    DEPARTMENT_CHOICES = EmailData.DEPARTMENT_CHOICES

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_schedules')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    subject = models.CharField(max_length=255, null=True)
    content = RichTextField(blank=True, null=True) 
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_sent = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.subject} - {self.user.email}" 
