# myapp/tasks.py

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from email_data.models import EmailData, Department
from coldemail import settings
from .models import EmailSchedule
from django.utils import timezone
from authentication.models import CustomUser

@shared_task(bind=True)
def send_department_emails_now(self, department_name, subject, content, user_email):
    try:
        # Mencari department berdasarkan nama
        department = Department.objects.get(nama=department_name)
    except Department.DoesNotExist:
        return f"Department with name '{department_name}' does not exist."

    recipients = EmailData.objects.filter(department=department)
    from_email = settings.EMAIL_HOST_USER

    for recipient in recipients:
        html_message = render_to_string('email_template.html', {'department': department_name, 'content': content, 'name': recipient.nama})
        send_mail(
            subject,
            '',
            from_email,
            [recipient.email],
            html_message=html_message,
            fail_silently=True, 
        )
        print(f'Email sent to {recipient.email}')

    schedule_time = timezone.now()

    try:
        user = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        user = None

    email_schedule = EmailSchedule(
        department=department,
        subject=subject,
        content=content,
        schedule_time=schedule_time,
        user=user,
        status_sent=True
    )
    email_schedule.save()
    return f"Emails sent to {department_name} department"

@shared_task(bind=True)
def send_department_emails(self, department_name, subject, content, id):
    try:
        # Mencari department berdasarkan nama
        department = Department.objects.get(nama=department_name)
    except Department.DoesNotExist:
        return f"Department with name '{department_name}' does not exist."
    
    recipients = EmailData.objects.filter(department=department) 
    html_message = render_to_string('email_template.html', {'department': department, 'content': content})
    from_email = settings.EMAIL_HOST_USER

    for recipient in recipients:
        send_mail(
            subject,
            '',
            from_email,
            [recipient.email],
            html_message=html_message,
            fail_silently=True, 
        )
    email_schedule = EmailSchedule.objects.get(id=id)
    email_schedule.status_sent = True
    email_schedule.save()

    return f"Emails sent to {department} department"