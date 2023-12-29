from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils import formats

from .utils import import_datetieme_format
from .models import Project, Task, TaskNote, ProjectNote

from django import forms

# class TaskFormForProjectAdmin(forms.ModelForm):
#     class Meta:
#         model = Task
#         exclude = ["user", "get_time_to_finish"]

def espected_finish(obj):
    """Returns the get_time_to_finish property of a TASK 
    in the same format of the other datetime fields."""

    format = import_datetieme_format(get_language())
    return formats.date_format(obj.get_time_to_finish, format=format)

def project_view(obj):
    url = reverse('progress:admin_project_view', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


class ProjectNoteAdmin(admin.StackedInline):
    """for see the projectNote form inside the ProjectAdmin"""
    readonly_fields = ["user"]

    model = ProjectNote
    extra = 1 

class TaskStackedAdmin(admin.StackedInline):
    """for see the task form inside the ProjectAdmin"""
    # form = TaskFormForProjectAdmin
    readonly_fields = ["created", "started", "completed", espected_finish]

    model = Task
    extra = 1

    

 

class TaskNoteStackedAdmin(admin.StackedInline):
    """for see the taskNoteStacked form inside the TaskAdmin"""
    # form = NoteTaskForm 
    readonly_fields = ["user"]
    model = TaskNote
    extra = 1

    ### this could be helpfull for single forms of admin.ModelAdmin
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ["project", "created", "started", "completed", espected_finish]
    inlines = [TaskNoteStackedAdmin]

    # Django Docs are Awesome
    # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_formset
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not instance.id:
                instance.user = request.user
            instance.save()
        # formset.save_m2m()
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', project_view, 'importance', 'status', 'created', ]
    filter_horizontal = ['users']
    search_fields = ['name', 'description']
    inlines = [ProjectNoteAdmin, TaskStackedAdmin]


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not instance.id:
                instance.user = request.user
            instance.save()
    