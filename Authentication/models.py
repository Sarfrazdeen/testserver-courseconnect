from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    Mobile_number = models.CharField(max_length=10, null=True, blank=True)
    Date_of_birth = models.DateField(null=True, blank=True)
    
    # Method to calculate age from Date_of_birth
    @property
    def Age(self):
        today = date.today()
        return today.year - self.Date_of_birth.year - ((today.month, today.day) < (self.Date_of_birth.month, self.Date_of_birth.day))

    def __str__(self):
        return self.username  # You can return the username or another field to represent the user
