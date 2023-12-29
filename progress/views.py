from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.http import HttpResponse, QueryDict
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django_htmx.http import retarget

from .models import Task, Project, TaskNote, ProjectNote
from .forms import NoteForm

def projects_home(request):
    template_name = 'progress/home.html'
    title = False

    if request.htmx:
        if request.htmx.current_url not in [request.build_absolute_uri(reverse('account:login_view')),
                                    request.build_absolute_uri(reverse('account:register_view'))]:

            template_name = 'progress/snippets/home.html'
            title = True

        # handeling LOGIN AND REGISTER redirection for get the entire page
        else:
            response = render(request, template_name, {'active_section':'home'})        
            return retarget(response, 'body')
        
    return render(request, template_name, {'active_section':'home', 'title':title})

def projects_all(request):
    """returns all the public projects and the
    current user private projects"""

    projects = Project.objects.filter(public=True)
    
    # get the private projects of this user
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(users__in=[request.user], public=False)
        if user_projects is not None:
            projects = projects | user_projects

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True
    else:
        template_name = 'progress/project_list.html'
        title = False

    return render(request, template_name, {'projects':projects, 'title':title, 'active_section':'all'})

def projects_public(request):
    """returns all the public projects"""
    projects = Project.objects.filter(public=True)

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True
    else:
        template_name = 'progress/project_list.html'
        title = False
    return render(request, template_name, {'projects':projects, 'active_section':'public', 'title':title})

@login_required
def projects_private(request):
    """returns the user private projects"""

    projects = Project.objects.filter(users__in=[request.user], public=False)

    if request.htmx:
        template_name = 'progress/snippets/project_list.html'
        title = True

    else:
        template_name = 'progress/project_list.html'
        title = False

    return render(request, template_name, {'projects':projects, 'active_section':'private', 'title':title})

def project_detail(request, project_id):
    """returns the detail project is it's public or if the 
    request user is the owner"""
    
    project = get_object_or_404(Project, id=project_id)

    if project.public:
        pass
    else: 
        # check if the user has permition to this project
        if not project.users.filter(id=request.user.id).exists():
            return HttpResponseForbidden()
        
    response = render(request, 'progress/project_detail.html', {'project':project, 'active_section':''})
    
    if request.htmx:
        return retarget(response, "body")
    return response

@staff_member_required
def admin_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "admin/progress/project/detail.html", {'project':project})

@login_required
def create_project_note(request, project_id):
    """handles creation and edition of ProjectNote
    returns a partial with the list of Notes for the Project"""
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['note']
            new_note = ProjectNote.objects.create(user=request.user, project=project, message=message)
            return render(request, "progress/snippets/project_note_list.html", {"object_notes_all": [new_note]})
        return HttpResponse('You need to put something as note message', status=400)
    

    if request.method == "PUT":
        data = QueryDict(request.body)
        note = get_object_or_404(ProjectNote, id=data.get('noteId'), user=request.user)
        form = NoteForm(data=data)
        if form.is_valid():
            note.message = form.cleaned_data.get('note')

            note.save()
            all_notes = note.project.project_notes.all()
            return render(request, "progress/snippets/project_note_list.html", {"object_notes_all": all_notes})
        return HttpResponse('You need to put something as note message', status=400)

    return HttpResponseNotAllowed('')

@login_required
def delete_project_note(request, note_id):
    """handles deletion of ProjectNote
    returns a partial with the list of remainder Notes for the Project"""
    note = get_object_or_404(ProjectNote, id=note_id, user=request.user)

    if request.method == "DELETE":
        project = note.project
        note.delete()

        remaind_notes = project.project_notes.all()
        return render(request, "progress/snippets/project_note_list.html", {"object_notes_all": remaind_notes})

   
    return HttpResponseNotAllowed('')


@login_required
def create_task_note(request, task_id):
    """handles creation and edition of TaskNote
    returns a partial with the list of Notes for the Task"""

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['note']
            new_note = TaskNote.objects.create(user=request.user, task=task, message=message)
            return render(request, "progress/snippets/task_note_list.html", {"object_notes_all": [new_note]})
        return HttpResponse('You need to put something as note message', status=400)
    

    if request.method == "PUT":
        data = QueryDict(request.body)
        note = get_object_or_404(TaskNote, id=data.get('noteId'), user=request.user)
        form = NoteForm(data=data)
        if form.is_valid():
            note.message = form.cleaned_data.get('note')

            note.save()
            all_notes = note.task.task_notes.all()
            return render(request, "progress/snippets/task_note_list.html", {"object_notes_all": all_notes})
        return HttpResponse('You need to put something as note message', status=400)

    return HttpResponseNotAllowed('')



@login_required
def delete_task_note(request, note_id):
    """handles creation and edition of TaskNote
    returns a partial with the list of remainder Notes for the Task"""
    note = get_object_or_404(TaskNote, id=note_id, user=request.user)
   
    if request.method == "DELETE":
        task = note.task
        note.delete()

        remaind_notes = task.task_notes.all()
        return render(request, "progress/snippets/task_note_list.html", {"object_notes_all": remaind_notes})
   
    return HttpResponseNotAllowed('')