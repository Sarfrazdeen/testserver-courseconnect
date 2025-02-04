from django import forms
from .models import contactus, Admission  # Ensure you are importing the Admission model
from phonenumber_field.formfields import PhoneNumberField

class ContactForm(forms.ModelForm):
    class Meta:
        model = contactus  # Ensure the model name matches your models.py
        fields = ['Full_name', 'Email', 'Phone_number', 'Message']  # Add 'Subject' to the fields

    Full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your name',
            'class': 'form-control'
        })
    )
    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    Phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',  # Adjust regex as needed
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'class': 'form-control'
        }),
        error_messages={
            'invalid': 'Enter a valid phone number (e.g., +123456789).'
        }
    )
    Message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your message',
            'class': 'form-control',
            'rows': 4
        })
    )

class AdmissionForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,  # Adjust maximum length for the phone number
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
        }),
        label="Phone Number"
    )

    class Meta:
        model = Admission
        fields = ['full_name', 'email', 'phone', 'course', 'message', 'created_by_user_id']  # Fields to include in the form

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: Any additional details or questions',
                'rows': 4,
            }),
        }

        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'course': 'Select Course',
            'message': 'Additional Information',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Default value for created_by_user_id if not provided
        instance.created_by_user_id = instance.created_by_user_id or 0
        if commit:
            instance.save()
        return instance
    
from django import forms
from .models import Admission

class AdForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['full_name', 'address', 'qualification', 'passed_out', 'passed_out_year',
                  'college_name', 'email', 'phone', 'course', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional Information (optional)'}),
            'passed_out': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = Admission.COURSE_CHOICES 
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if not self.instance or not self.instance.passed_out:
            self.fields['passed_out_year'].required = False
            self.fields['passed_out_year'].widget = forms.HiddenInput()
        else:
            self.fields['passed_out_year'].widget.attrs.update({'class': 'form-control'})