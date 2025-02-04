from django.db import models
from django.utils.timezone import now
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField  # Install django-phonenumber-field
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

class contactus(models.Model):
    Full_name = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone_number = models.CharField(max_length=15)
    Message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Finished', 'Finished')],
        default='Pending'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='updated_contacts'
    )
    modified_date = models.DateTimeField(null=True, blank=True)
    submission_date = models.DateTimeField(default=now)
    
class Admission(models.Model):
    COURSE_CHOICES = [
        ('C_programming', 'C Programming'),
        ('Python_programming', 'Python Programming'),
        ('Java_programming', 'Java Programming'),
        ('React_js', 'React JS'),
        ('Front_end_development', 'Front End Development'),
        ('Web_development', 'Full Stack Web Development'),
        ('Civil_cad', 'Civil CAD'),
        ('Mechanical_cad', 'Mechanical CAD'),
        ('Digital_marketing', 'Digital Marketing'),
        ('Graphic_design', 'Graphic Design'),
        ('Other', 'Other Programs'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('on_progress', 'On Progress'),
        ('finished', 'Finished'),
    ]

    # Core fields
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    qualification = models.CharField(max_length=150, verbose_name="Qualification")
    passed_out = models.BooleanField(default=False, verbose_name="Passed Out")
    passed_out_year = models.IntegerField(null=True, blank=True, verbose_name="Passed Out Year")
    college_name = models.CharField(max_length=150, verbose_name="College Name")
    email = models.EmailField(verbose_name="Email Address", unique=False)
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, verbose_name="Selected Course")
    course_duration = models.CharField(max_length=100, verbose_name="Course Duration")
    message = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Submission Date")

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")

    # Audit fields
    created_by_user_id = models.IntegerField(null=True, blank=True, verbose_name="Created By User ID")
    created_date = models.DateTimeField(default=now, verbose_name="Created Date")
    modified_by_user_id = models.IntegerField(null=True, blank=True, verbose_name="Modified By User ID")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Modified Date")

    def clean(self):
        if self.passed_out and not self.passed_out_year:
            raise ValidationError("Passed Out Year is required if Passed Out is selected.")
        if not self.passed_out and self.passed_out_year:
            raise ValidationError("Passed Out Year cannot be provided if Passed Out is not selected.")

    def __str__(self):
        return f'{self.full_name} - {self.course}'

    class Meta:
        ordering = ['-submission_date']
        verbose_name = "Admission"
        verbose_name_plural = "Admissions"