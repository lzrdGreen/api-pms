from django.db import models
from datetime import date
import datetime
from django.core.exceptions import ValidationError


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #progress = models.FloatField(default=0)    

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')

    
    def __str__(self):
        return f'{self.title}'
      
    def is_overdue(self):
        return self.due_date < date.today() and self.status != 'done'
    