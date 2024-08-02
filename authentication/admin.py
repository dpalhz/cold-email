from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_at', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    readonly_fields = ('created_at',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
