from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Project, Task
from datetime import date
import datetime

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'start_date', 'due_date'] 
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project or getattr(self.instance, 'project', None)
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        status = cleaned_data.get('status')
        #project = cleaned_data.get('project') # get the project from the form

        if self.project and start_date and start_date < self.project.created_at.date():
            self.add_error('start_date', 'Start date cannot be before the project\'s creation date.')

        if not self.instance.pk and start_date and start_date < date.today():
            self.add_error('start_date', 'Start date cannot be in the past.')

        if due_date and start_date and due_date < start_date:
            self.add_error('due_date', 'Due date must be after start date.')

        if due_date and due_date < date.today() and status != 'done':
            self.add_error('due_date', 'This task is overdue and must be marked as "Done" or the due date must be updated.')

        return cleaned_data
