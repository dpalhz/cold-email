# urls.py
from django.urls import path
from .views import schedule_email_post
app_name = 'sendingemail'

urlpatterns = [
    path('schedule-email/', schedule_email_post, name='schedule_email'),
]
