from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import EmailData, Department
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages
import pandas as pd
from django.core.files.storage import default_storage
import os


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


def bulk_add_email(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect('email_data:email_list')

        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension not in ['.csv', '.xls', '.xlsx']:
            messages.error(request, "Unsupported file format. Please upload a CSV or Excel file.")
            return redirect('email_data:email_list')

        try:
            # Process the file directly from memory
            if file_extension == '.csv':
                df = pd.read_csv(file)
            else:  # Assuming it's an Excel file
                df = pd.read_excel(file)

            # Validate the columns
            required_columns = {'nama', 'email', 'department'}
            if not required_columns.issubset(df.columns):
                messages.error(request, "The uploaded file is missing required columns.")
                return redirect('email_data:email_list')

            for _, row in df.iterrows():
                department_name = row.get('department', '')
                department, created = Department.objects.get_or_create(nama=department_name)
                EmailData.objects.create(
                    nama=row.get('nama', ''),
                    email=row.get('email', ''),
                    department=department
                )

            messages.success(request, "Emails added successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('email_data:email_list')



def download_template(request):
    # Create a DataFrame for the Excel template
    data = {
        'nama': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com'],
        'department': ['IT', 'HR']
    }
    df = pd.DataFrame(data)

    # Convert DataFrame to an Excel file in memory
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=email_template.xlsx'
    df.to_excel(response, index=False)

    return response