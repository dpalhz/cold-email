from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Access restricted to admin users only.')
        else:
            messages.error(request, 'The email or password is incorrect!')
    context = {}
    return render(request, 'login.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return render(request, 'register.html')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('authentication:login')


def forgot_password(request):
    context = {}
    return render(request, 'forgotpassword.html', context)
