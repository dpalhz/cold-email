from django import forms
from sendingemail.models import EmailSchedule
from ckeditor.widgets import CKEditorWidget

class EmailScheduleForm(forms.ModelForm):
    class Meta:
        model = EmailSchedule
        fields = ['department', 'subject', 'content', 'schedule_time']
        widgets = {
            'content': CKEditorWidget(),
        }
