from django.urls import path
from . import views


app_name = 'generator_message'

urlpatterns = [
    path('', views.generator_view , name="generator"),
    path('chat/', views.chat, name='chat'),
]