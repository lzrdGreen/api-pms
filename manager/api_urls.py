from django.urls import path
from .api_views import ProjectsView, TasksView, SingleProjectView, SingleTaskView

urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('tasks/', TasksView.as_view()),
    path('projects/<int:pk>', SingleProjectView.as_view()),
    path('tasks/<int:pk>/',SingleTaskView.as_view())
]