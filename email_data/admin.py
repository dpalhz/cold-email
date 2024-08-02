from django.contrib import admin
from .models import EmailData

class EmailDataAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'group', 'created_at', 'updated_at')
    search_fields = ('nama', 'email', 'group')
    list_filter = ('group', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(EmailData, EmailDataAdmin)
