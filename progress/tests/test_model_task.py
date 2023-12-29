from datetime import timedelta, timezone
from django.utils import timezone as tz
from django.test import TestCase
from progress.models import Task, Project

class TaskTests(TestCase):
    def setUp(self):
        project_required_data = {
            'name': 'project test',
            'description': 'description of my project',
        }
        self.project = Project.objects.create(**project_required_data)

        task_required_data = {
            'name' : 'my task',
            'description' : '',
            'project' : self.project
        }

        task_working_status = {
            'name' : 'my task 2',
            'description' : 'this is my second task',
            'project' : self.project,
            'status' : Task.Status.WORKING,
            'estimated_time': 2,
        }
        self.task = Task.objects.create(**task_required_data)
        self.task2 = Task.objects.create(**task_working_status)

    def test_required_data(self):
        """checking the required data for create tasks and projects"""
        self.assertIsInstance(self.task, Task)
        self.assertIsInstance(self.project, Project)

    def test_task_default_values(self):
        """checks the expected value dates """
        self.assertIsNone(self.task.started)
        self.assertIsNone(self.task.completed)
        self.assertIsNone(self.task.estimated_time)
        self.assertEqual(self.task.esitmated_unit_time, Task.UnitTime.HOUR)

        # get_time_to_finish is not None only when started exists and completed is None
        self.assertIsNone(self.task.get_time_to_finish)

        
        # important default value of status is PENDING
        self.assertEqual(self.task.status, Task.Status.PENDING)
        self.assertEqual(self.task.importance, Task.Importance.NORMAL)
        self.assertEqual(self.task.created.replace(second=0, microsecond=0),
                          tz.now().replace(second=0, microsecond=0))

    def test_task_change_status_to_wroking(self):
        """changes on status must update the values of started and completed"""
        
        # by default started is None
        self.assertIsNone(self.task.started)
        
        self.task.status = Task.Status.WORKING
        self.task.save()
        
        # after save started has been "created"
        self.assertIsNotNone(self.task.started)

        self.assertEqual(self.task.started.replace(second=0, microsecond=0),
                          tz.now().replace(second=0, microsecond=0))
        
    def test_task2_change_status_working_to_completed(self):
        """changes on status must update the values of started and completed"""

        # it has been created with status WORKING so created exists
        self.assertIsNotNone(self.task2.started)
        self.assertIsNone(self.task2.completed)

        # when change status to COMPLETED completed is created
        self.task2.status = Task.Status.COMPLETED
        self.task2.save()
        self.assertIsNotNone(self.task2.completed)

        # if change status from COMPLETED to WAITING started and completed 
        # are set to None
        self.task2.status = Task.Status.PENDING
        self.task2.save()
        self.assertIsNone(self.task2.started)
        self.assertIsNone(self.task2.completed)

    def test_task2_get_time_to_finish(self):
        """checks the calculation time of get_time_to_finish"""
        self.assertIsNotNone(self.task2.get_time_to_finish)

        # the default unit time is hours
        prevition_task = self.task2.started + timedelta(hours=self.task2.estimated_time)

        # must be equal to started + stimated_time    
        self.assertEqual(self.task2.get_time_to_finish, prevition_task)
        
        # must be diferent to started time
        self.assertNotEqual(self.task2.get_time_to_finish, self.task2.started) 

    def test_timezone_get_time_to_finish(self):
        """all dates are time-zone utc (the convertion is handel by django)
        except get_time_to_finish that uses by default the project time-zone"""
        
        # started is in utc
        self.assertEquals(self.task2.started.tzinfo, timezone.utc)
        # get_time_to_finish is in current timezone
        self.assertEquals(self.task2.get_time_to_finish.tzinfo, tz.get_current_timezone())

        # started and get_time_to_finish are in different timezones
        self.assertNotEquals(self.task2.started.tzinfo, self.task2.get_time_to_finish.tzinfo)