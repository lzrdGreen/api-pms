from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Project, Task #, TaskDependency
from .forms import ProjectForm, TaskForm

# Home page
def main(request):
    return render(request, 'manager/main.html')

# Create project using CreateView
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'manager/project_form.html'
    success_url = reverse_lazy('project_list') #Where to redirect afterwards

# Edit project using UpdateView
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'manager/project_form.html'
    success_url = reverse_lazy('project_list') #Where to redirect afterwards
    pk_url_kwarg = 'id'

# List all projects using ListView
class ProjectListView(ListView):
    model = Project
    template_name = 'manager/project_list.html'
    context_object_name = 'projects'  # default is object_list

# View the details of a project using DetailView
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'manager/project_detail.html'
    context_object_name = 'project'  # default is object
    pk_url_kwarg = 'id'

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'manager/project_confirm_delete.html'
    success_url = reverse_lazy('project_list') #Where to redirect afterwards
    pk_url_kwarg = 'id'
    
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'manager/task_create_form.html'

    def get_success_url(self):
        project_id = self.kwargs['project_id']
        return reverse('project_detail', kwargs={'id': project_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return kwargs
    
    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().form_valid(form)

"""
    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        response = super().form_valid(form)
        parents = form.cleaned_data.get('parents')
        if parents:
            TaskDependency.objects.bulk_create([
                TaskDependency(task=self.object, dependency=parent) for parent in parents
            ])
        return response
"""


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'manager/task_update_form.html'
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        project_id = self.object.project.id
        return reverse('project_detail', kwargs={'id': project_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project 
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_object().project
        return kwargs
"""   
    def form_valid(self, form):
        response = super().form_valid(form)
        parents = form.cleaned_data.get('parents')

        # Remove old dependencies
        TaskDependency.objects.filter(task=self.object).delete()

        # Add updated ones
        if parents:
            TaskDependency.objects.bulk_create([
                TaskDependency(task=self.object, dependency=parent) for parent in parents
            ])
        return response
"""


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'manager/task_confirm_delete.html'
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'id': self.object.project.id})

class TaskDetailView(DetailView):
    model = Task
    template_name = 'manager/task_detail.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'

class TaskListView(ListView):
    # This view has no urlpattern in urls.py
    # So it is redundant
    # But it might be needed for complex filtering, sorting, or pagination to the task list
    # When building an API, you might use TaskListView to provide a JSON or XML representation of the task list. (API Endpoints)
    model = Task
    template_name = 'manager/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context