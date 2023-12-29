from django.urls import path 
from . import views
from django.views.generic import TemplateView

app_name = 'progress'
urlpatterns = [
    path('progress/admin/project/<int:project_id>/', views.admin_project_view, name="admin_project_view"),
    path('projects/all/', views.projects_all, name="projects_all"),
    path('projects/public/', views.projects_public, name="projects_public"),
    path('projects/private/', views.projects_private, name="projects_private"),
    path('project/<int:project_id>/', views.project_detail, name="project_detail"),

    # curl
    path('project/create-note/<int:project_id>/', views.create_project_note, name="create_project_note"),
    path('task/create-note/<int:task_id>/', views.create_task_note, name="create_task_note"),

    path('project/note/<int:note_id>/', views.delete_project_note, name="delete_project_note"),
    path('task/note/<int:note_id>/', views.delete_task_note, name="delete_task_note"),


    path('', views.projects_home, name='projects_home'),
]