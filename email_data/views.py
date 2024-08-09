from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import EmailData, Department
from django.contrib.admin.views.decorators import staff_member_required

from .forms import EmailDataForm, DepartmentForm
@staff_member_required(login_url='/auth/login/')
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Department created successfully!'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

@staff_member_required(login_url='/auth/login/')
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Untuk permintaan GET, berikan data department dalam bentuk JSON
        department_data = {
            'nama': department.nama,
            'deskripsi': department.deskripsi,
        }
        return JsonResponse(department_data)

@staff_member_required(login_url='/auth/login/')
def delete_department(request, pk):
    try:
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@staff_member_required(login_url='/auth/login/')
def email_list(request):
    emails = EmailData.objects.all()
    department = Department.objects.all()
    return render(request, 'email_list.html', {'emails': emails, 'departments' : department})

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

