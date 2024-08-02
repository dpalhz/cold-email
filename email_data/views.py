from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmailDataForm
from django.http import JsonResponse
from .models import EmailData
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='/auth/login/')
def email_list(request):
    emails = EmailData.objects.all()
    return render(request, 'email_list.html', {'emails': emails})

@staff_member_required(login_url='/auth/login/')
def email_detail(request, email):
    email_data = get_object_or_404(EmailData, email=email)
    return render(request, 'email_detail.html', {'email_data': email_data})

@staff_member_required(login_url='/auth/login/')
def email_create(request):
    if request.method == "POST":
        form = EmailDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_data:email_list')
    else:
        form = EmailDataForm()
    return render(request, 'email_form.html', {'form': form})

@staff_member_required(login_url='/auth/login/')
def email_update(request, email):
    email_data = get_object_or_404(EmailData, email=email)
    if request.method == "POST":
        form = EmailDataForm(request.POST, instance=email_data)
        if form.is_valid():
            form.save()
            return redirect('email_data:email_list')
    else:
        form = EmailDataForm(instance=email_data)
    return render(request, 'email_form.html', {'form': form})

@staff_member_required(login_url='/auth/login/')
def email_delete(request, email):
    email_data = get_object_or_404(EmailData, email=email)
    if request.method == "POST":
        email_data.delete()
        return redirect('email_data:email_list')
    return render(request, 'email_confirm_delete.html', {'email_data': email_data})


@staff_member_required(login_url='/auth/login/')
def get_all_emails(request):
    emails = EmailData.objects.all().values('nama', 'email', 'created_at', 'updated_at', 'group')
    return JsonResponse(list(emails), safe=False)

@staff_member_required(login_url='/auth/login/')
def get_emails_by_department(request, department):
    emails = EmailData.objects.filter(group=department).values('nama', 'email', 'created_at', 'updated_at', 'group')
    return JsonResponse(list(emails), safe=False)
