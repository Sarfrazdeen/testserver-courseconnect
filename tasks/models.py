from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status_choices = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Not Started')

    def __str__(self):
        return self.title

    def update_status(self):
        if self.completed_date and self.completed_date <= timezone.now().date():
            self.status = 'Completed'
        elif self.start_date <= timezone.now().date() <= self.end_date:
            self.status = 'In Progress'
        else:
            self.status = 'Not Started'
        self.save()

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)
