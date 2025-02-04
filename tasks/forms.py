from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date', 'completed_date']

    # Optional: Custom validation if needed
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date < self.cleaned_data['start_date']:
            raise forms.ValidationError("End date cannot be earlier than the start date.")
        return end_date
