from django.urls import path
from . import views
from . import www_views

urlpatterns = [
    path('', views.main, name='home_page'),
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/edit/<int:id>/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('project/<int:id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/delete/<int:id>/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:project_id>/task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/edit/<int:task_id>/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/delete/<int:task_id>/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    
    # Static HTML API-driven frontend (WWW views)
    path('static-site/projects/', www_views.project_list_static, name='static_project_list'),
    path('static-site/new-project/', www_views.project_form_static, name='static_project_form'),
    path('static-site/', www_views.index_static, name='static_index'),
    path('static-site/task_detail.html', www_views.task_detail_static, name='static_task_detail'),
    path('static-site/tasks/<int:task_id>/', www_views.task_detail_static_dynamic, name='static_task_detail_dynamic'),
    #path('static-site/tasks/<int:task_id>/', www_views.task_detail_static, name='static_task_detail'),
    #path('static-site/task_detail.html', www_views.task_detail_static, name='static_task_detail'),
]

