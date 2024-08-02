from django.contrib import admin
from .models import EmailSchedule
from .forms import EmailScheduleForm

@admin.register(EmailSchedule)
class EmailScheduleAdmin(admin.ModelAdmin):
    form = EmailScheduleForm
    list_display = ('department', 'subject', 'schedule_time', 'status_sent', 'created_at', 'updated_at')
    search_fields = ('department', 'subject')
    list_filter = ('department', 'schedule_time', 'status_sent')
