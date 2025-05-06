from rest_framework import generics
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectsView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class SingleProjectView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class SingleTaskView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
"""
class TasksView(generics.ListCreateAPIView):
queryset = Task.objects.all()
serializer_class = TaskSerializer
"""

class TasksView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id is not None:
            queryset = queryset.filter(project=project_id)
        return queryset