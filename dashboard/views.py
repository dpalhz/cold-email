from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from sendingemail.models import EmailSchedule
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from sendingemail.forms import EmailScheduleForm
from django.utils import timezone
import json
import pytz

from django.views.decorators.csrf import csrf_exempt

@staff_member_required(login_url='/auth/login/')
def home(request):
    return render(request, "email_manager.html")

def format_schedule_time(utc_time):
    jakarta_timezone = pytz.timezone('Asia/Jakarta')
    return utc_time.astimezone(jakarta_timezone)

@staff_member_required(login_url='/auth/login/')
def get_sent_emails(request):
    sent_emails = EmailSchedule.objects.filter(schedule_time__lte=timezone.now(), user=request.user, status_sent=True)
    data = {
        'emails': [{'id': email.id, 'subject': email.subject, 'schedule_time': format_schedule_time(email.schedule_time).strftime("%d-%m-%Y %H:%M:%S")} for email in sent_emails],
    }
    return JsonResponse(data)

@staff_member_required(login_url='/auth/login/')
def get_scheduled_emails(request):
    scheduled_emails = EmailSchedule.objects.filter(schedule_time__gt=timezone.now(), user=request.user, status_sent=False)
    data = {
        'emails': [{'id': email.id, 'subject': email.subject, 'schedule_time': format_schedule_time(email.schedule_time).strftime("%d-%m-%Y %H:%M:%S")} for email in scheduled_emails],
    }
    return JsonResponse(data)

@staff_member_required(login_url='/auth/login/')
def get_email_details(request, pk):
    email = get_object_or_404(EmailSchedule, pk=pk)
    email_details = {
        'id': str(email.id),
        'department': email.department,
        'subject': email.subject,
        'content': email.content,
        'schedule_time': format_schedule_time(email.schedule_time).strftime("%d-%m-%Y %H:%M:%S")
    }
    return JsonResponse(email_details)

@staff_member_required(login_url='/auth/login/')
def edit_schedule_email_view(request, pk):
    email_schedule = get_object_or_404(EmailSchedule, pk=pk)
    if email_schedule.status_sent:
        return JsonResponse({'success': False, 'errors': form.errors})


    old_department = email_schedule.department
    old_schedule_time = email_schedule.schedule_time

    if request.method == 'POST':
        form = EmailScheduleForm(request.POST, instance=email_schedule)
        
        if form.is_valid():
            email_schedule = form.save(commit=False)
            schedule_time = email_schedule.schedule_time

            # Update the periodic task with new crontab schedule and args
            day_of_week = schedule_time.weekday() + 1
            if day_of_week == 7:
                day_of_week = 0

            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=schedule_time.minute,
                hour=schedule_time.hour,
                day_of_month=schedule_time.day,
                month_of_year=schedule_time.month,
                day_of_week=day_of_week
            )

            # Get the old periodic task and update it
            old_task_name = f"Send email to {old_department} at {format_schedule_time(old_schedule_time)} - ID: {email_schedule.id}"
            periodic_task = get_object_or_404(PeriodicTask, name=old_task_name)
            
            # Save changes to email_schedule first
            email_schedule.save()

            # Update the name, crontab, args, and expiration
            new_task_name = f"Send email to {email_schedule.department} at {format_schedule_time(schedule_time)} - ID: {email_schedule.id}"
            periodic_task.name = new_task_name
            periodic_task.crontab = schedule
            periodic_task.args = json.dumps([email_schedule.department, email_schedule.subject, email_schedule.content, str(email_schedule.id)])
            periodic_task.expires = schedule_time + timezone.timedelta(minutes=10)
            periodic_task.save()

            return JsonResponse({'success': True, 'message': 'Email schedule updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EmailScheduleForm(instance=email_schedule)
    return render(request, 'edit_schedule_email.html', {'form': form, 'email_schedule': email_schedule})

@staff_member_required(login_url='/auth/login/')
@csrf_exempt
def delete_email(request, pk):
    if request.method == 'POST':
        email = get_object_or_404(EmailSchedule, pk=pk)

        periodic_task = PeriodicTask.objects.filter(
            name=f"Send email to {email.department} at {format_schedule_time(email.schedule_time)} - ID: {email.id}"
        ).first()

        if not periodic_task:
            email.delete()
            return JsonResponse({'status': 'success'}, status=200)
        
        email.delete()
        periodic_task.delete()
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)
