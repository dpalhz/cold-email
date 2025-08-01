from django.urls import path
from . import views

app_name = 'email_data'

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('email/new/', views.email_create, name='email_create'),  # Pastikan URL pattern untuk create ada di sini
    path('email/<str:email>/edit/', views.email_update, name='email_update'),
    path('email/<str:email>/delete/', views.email_delete, name='email_delete'),
    path('api/emails/', views.get_all_emails, name='get_all_emails'),
    path('api/emails/department/<str:department>/', views.get_emails_by_department, name='get_emails_by_department'),
    path('department/create/', views.create_department, name='department_create'),
    path('department/edit/<uuid:pk>/', views.edit_department, name='department_edit'),
    path('department/delete/<uuid:pk>/', views.delete_department, name='department_delete'),
    path('bulk-add-email/', views.bulk_add_email, name='bulk_add_email'),
    path('download-template/', views.download_template, name='download_template'),
]
