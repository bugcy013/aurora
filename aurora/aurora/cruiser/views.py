from models import Project, Task
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import aurora.settings as settings
from django.http import HttpResponseRedirect
from django.core import urlresolvers


@render_to('base.html')
def index(request):
    pass
    return {}


@render_to('project.html')
def project(request, project_id):
    from models import Stage, Deploy
    project = get_object_or_None(Project, id=project_id)
    if not project:
        return {}
    else:
        stages = Stage.objects.filter(project=project).order_by('name',)
        deployments = Deploy.objects.filter(stage__in=stages).order_by('-finished_at',)
        return {'p': project, 'stages': stages, 'deps': deployments}


def new_project(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:cruiser_project_add'))


@render_to('task.html')
def task(request, task_id):
    task = get_object_or_None(Task, id=task_id)
    if not task:
        return {}
    else:
        return {'task': task}


@render_to('500.html')
def server_error(request):
    return {'STATIC_URL': settings.STATIC_URL}
