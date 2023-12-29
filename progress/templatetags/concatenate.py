from django import template
register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_completed_tasks(project):
    """returns the number of completed task in a project"""
    return project.tasks.filter(status=4).count()

@register.filter
def get_uncompleted_tasks(project):
    """returns the number of uncompleted task in a project"""
    return project.tasks.filter(status__lt=4).count()