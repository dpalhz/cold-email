from django.contrib import admin
from .models import EmailData, Department

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('nama', 'deskripsi', 'created_at', 'updated_at')
    search_fields = ('nama',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Department, DepartmentAdmin)

class EmailDataAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'department', 'created_at', 'updated_at')
    search_fields = ('nama', 'email', 'department__nama')
    list_filter = ('department', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(EmailData, EmailDataAdmin)
