from datetime import timedelta
from django.db import models
from django.urls import reverse
from django.utils import timezone as tz
from django.core.exceptions import ValidationError

from account.models import User


class Project(models.Model):
    class Importance(models.IntegerChoices):
        LOW = (1, 'Low')
        INTERESTIG = (2, 'Interesting')
        NORMAL = (3, 'Normal')
        IMPORTANT = (4, 'Importat')
        URGENT = (5, 'Urgent')       

    class Status(models.IntegerChoices):
        IDEA = (1, 'Proccessing the requirements')
        DESING = (2, 'Desiging the user interaction')
        DEVELOPING = (3, 'Developing first version')
        IMPLEMENTIG = (4, 'Deploying first version')
        ITERATING = (5, 'Adding more requirements')
        COMPLETED = (6, 'Completed')


    name = models.CharField(max_length=120)
    description = models.TextField()
    importance = models.IntegerField(choices=Importance.choices, default=Importance.NORMAL)
    status = models.IntegerField(choices=Status.choices, default=Status.IDEA)
    image = models.FileField(upload_to='projects', null=True, blank=True)
    users = models.ManyToManyField(User, related_name="projects" , blank=True) 
    url = models.URLField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-importance', '-status', '-created']
        indexes = [models.Index(
            fields=['-importance', '-status', '-created']
        )]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('progress:project_detail', args=[self.id])
    
    

class Task(models.Model):
    class Importance(models.IntegerChoices):
        LOW = (1, 'Low')
        NORMAL = (2, 'Normal')
        IMPORTANT = (3, 'Importat')
        URGENT = (4, 'Urgent')       

    class Status(models.IntegerChoices):
        PENDING = (1, 'Not started yet')
        WORKING = (2, 'Working on it')
        WAITING = (3, 'Waiting feed back')
        COMPLETED = (4, 'Completed')

    class UnitTime(models.TextChoices):
        HOUR = ('H', 'Hour')
        DAY = ('D', 'Day')

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    importance = models.IntegerField(choices=Importance.choices, default=Importance.NORMAL)

    estimated_time = models.PositiveIntegerField(null=True)
    esitmated_unit_time = models.CharField(max_length=1, choices=UnitTime.choices,
                                           default=UnitTime.HOUR)
    
    started = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    __original_status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        """updates the started and completed dateTime
        in relation to previous a new status"""

        # no changes
        if self.id and self.status == self.__original_status:
            pass

        # new task
        elif not self.id:
            if self.status == self.Status.WORKING:
                self.started = tz.now()

            elif self.status == self.Status.COMPLETED:
                self.started = tz.now()
                self.completed = tz.now()

        # old task marked previously as NOT WORKING. 
        elif self.__original_status != self.Status.WORKING:

            # if previously state was COMPLETED set both to None 
            if self.__original_status == self.Status.COMPLETED:
                self.started = None
                self.completed = None

            if self.status == self.Status.WORKING:
                self.started = tz.now()

            elif self.status == self.Status.COMPLETED:
                self.started = tz.now()
                self.completed = tz.now()

        # old task marked previously as WORKING. 
        elif self.__original_status == self.Status.WORKING:

            # if new status is COMPLETED 
            if self.status == self.Status.COMPLETED:
                self.completed = tz.now()

            # if new status is PENDING or WAITING
            elif self.status in [self.Status.COMPLETED, self.Status.WAITING]:
                self.started = None
                self.completed = None

        super(Task, self).save(*args, **kwargs)
        self.__original_status = self.status



    @property
    def get_time_to_finish(self):
        """returns the previst datetime to finish the task
        based in: started, estimated_time and esitmated_unit_time"""
        if not self.started or not self.estimated_time or not self.esitmated_unit_time:
            return None
        if self.started and self.completed:
            return None
        if self.esitmated_unit_time == self.UnitTime.HOUR:
            estimated_finish = self.started + timedelta(hours=self.estimated_time)
        else:
            estimated_finish = self.started + timedelta(days=self.estimated_time)

        return estimated_finish.astimezone(tz.get_current_timezone())

    class Meta:
        ordering = ['-created', '-importance', '-status',]
        indexes = [models.Index(
            fields=['-created', '-importance', '-status']
        )]

    def __str__(self):
        return f'{self.name} from Proyect: {self.project}'
    
class AbstractNote(models.Model):
    """for use as base of ProjectNote and TaskNote"""
    message = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'writed on {self.created.strftime("%d/%m/%Y %I:%M%p")}'

class ProjectNote(AbstractNote):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_notes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="project_notes",
                             blank=True)
    
    def was_updated(self):
        """for show the updated date only when it was updated"""
        created = self.created.replace(second=0, microsecond=0)
        updated = self.updated.replace(second=0, microsecond=0)

        return created != updated
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(
            fields=['created']
        )]

class TaskNote(AbstractNote):
    task = models.ForeignKey(Task,
                                on_delete=models.CASCADE,
                                related_name='task_notes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="task_notes",
                             blank=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(
            fields=['created']
        )]
