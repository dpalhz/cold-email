from django.urls import path
from .views import login_user, logout_user, register_user, forgot_password
from django.contrib.auth import views
from django.urls import reverse_lazy

app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('password_reset/', views.PasswordResetView.as_view(template_name="Password_Reset_Form.html",   email_template_name='password_reset_email.html',
                                              success_url=reverse_lazy('authentication:password_reset_done')), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name="Password_Reset_Done.html"), name='password_reset_done'),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name="Password_Reset_Confirm.html", success_url=reverse_lazy('authentication:password_reset_complete')),
        name="password_reset_confirm",
    ),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name="Password_Reset_Complete.html"), name='password_reset_complete'),
]
