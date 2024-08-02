from django.urls import path
from .views import home, get_sent_emails, get_scheduled_emails, get_email_details, edit_schedule_email_view, delete_email


app_name = 'dashboard'

urlpatterns = [
    path('', home , name="home"),
    path('emails/sent/', get_sent_emails, name='get_sent_emails'),
    path('emails/scheduled/', get_scheduled_emails, name='get_scheduled_emails'),
    path('emails/detail/<uuid:pk>/', get_email_details, name='get_email_details'),
    path('edit-schedule-email/<uuid:pk>/', edit_schedule_email_view, name='edit_schedule_email'),
    path('emails/delete/<uuid:pk>/', delete_email, name='delete_email'),
  
]