# manager/www_views.py
from django.shortcuts import render

def project_list_static(request):
    return render(request, 'static_site/project_list.html')

def project_form_static(request):
    return render(request, 'static_site/project_form.html')

def index_static(request):
    return render(request, 'static_site/index.html')

def task_detail_static(request, task_id):
    return render(request, 'static_site/task_detail.html', {'task_id': task_id})

def task_detail_static_dynamic(request, task_id):
    return render(request, 'static_site/task_detail.html')