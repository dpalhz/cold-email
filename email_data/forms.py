from django import forms
from .models import EmailData

class EmailDataForm(forms.ModelForm):
    class Meta:
        model = EmailData
        fields = ['nama', 'email', 'group']

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
