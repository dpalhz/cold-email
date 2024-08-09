from django import forms
from .models import EmailData, Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['nama', 'deskripsi']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if Department.objects.filter(nama=nama).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Department with this name already exists.')
        return nama

class EmailDataForm(forms.ModelForm):
    class Meta:
        model = EmailData
        fields = ['nama', 'email', 'department']

    def __init__(self, *args, **kwargs):
        super(EmailDataForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk is None:
            if EmailData.objects.filter(email=email).exists():
                raise forms.ValidationError('Email data with this Email already exists.')
        else:
            if EmailData.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Email data with this Email already exists.')
        return email


class BulkEmailUploadForm(forms.Form):
    file = forms.FileField(label='Select a CSV or Excel file')