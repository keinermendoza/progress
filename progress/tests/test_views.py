from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from progress.models import Project


class TestProjectViews(TestCase):
    def setUp(self):
        
        self.client = Client()

        # creating users
        data_user_one = {
            'username': 'User one',
            'email': 'iliketodoprojects@gmail.com',
            'password': 'password'
        }
        data_user_two = {
            'username': 'User two',
            'email': 'imatwouser@gmail.com',
            'password': 'password'
        }
        data_user_admin = {
            'username': 'ADMIN',
            'email': 'superadmin@gmail.com',
            'password': 'admin_password',
            'is_staff': True,
            'is_superuser': True
        }

        self.user_one = User.objects.create(**data_user_one)        
        self.user_two = User.objects.create(**data_user_two)        
        self.user_admin = User.objects.create(**data_user_admin)        

        # creating projects
        data_public_project_1 = {
            # 'user': self.user_one,
            'name': 'public project',
            'description': 'description of my test project',
        }

        data_private_project_1 = {
            # 'user': self.user_one,
            'public': False,
            'name': 'public project',
            'description': 'description of my test project',
        }

        data_private_project_2 = {
            # 'user': self.user_two,
            'public': False,
            'name': 'public project',
            'description': 'description of my test project',
        }
        self.public_project_1 = Project.objects.create(**data_public_project_1)
        self.public_project_1.users.set([self.user_one])

        self.private_project_1 = Project.objects.create(**data_private_project_1)
        self.private_project_1.users.set([self.user_one])

        self.private_project_2 = Project.objects.create(**data_private_project_2)
        self.private_project_2.users.set([self.user_two])


        self.routes = {
            'home': reverse('progress:projects_home'),
            'all': reverse('progress:projects_all'),
            'public': reverse('progress:projects_public'),
            'private': reverse('progress:projects_private'),
            'detail_public_1': reverse('progress:project_detail', args=[self.public_project_1.id]),
            'detail_private_1': reverse('progress:project_detail', args=[self.private_project_1.id]),
            'detail_private_2': reverse('progress:project_detail', args=[self.private_project_2.id]),
            'admin_view': reverse('progress:admin_project_view', args=[self.private_project_1.id]),
        }

        self.use_HTMX = {'HTTP_HX-Request': 'true'}
        
        # the request_factory is giving me and error so i used this for avoid it
        self.DONT_use_HTMX = {'HTTP_HX-Request': 'false'}


    def test_configuration(self):
        """checks the setUp is correct"""
        self.assertIsInstance(self.user_one, User)
        self.assertIsInstance(self.user_two, User)
        self.assertIsInstance(self.user_admin, User)
        self.assertTrue(self.user_admin.is_superuser)

        self.assertIsInstance(self.public_project_1, Project)
        self.assertIsInstance(self.private_project_1, Project)
        self.assertIsInstance(self.private_project_2, Project)

    ### HOME VIEW
    def test_user_anonimous_get_home(self):
        """anonimous user can requests the home view"""
        
        response = self.client.get(self.routes['home'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/base.html')
        self.assertTemplateUsed(response, 'progress/home.html')

    def test_user_anonimous_get_home_using_HTMX(self):
        """anonimous user can requests the home view USING HTMX
        the response is a partial html"""

        response = self.client.get(self.routes['home'], **self.use_HTMX)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('progress/base.html', response.templates)
        self.assertTemplateUsed(response, 'progress/snippets/home.html')


    ### PROJECTS PUBLIC VIEW

    def test_user_anonimous_get_projects_public(self):
        """anonimous user can requests the projects_public view
        response contains only the public projects"""
        
        self.client.force_login(self.user_two)
        response = self.client.get(self.routes['public'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_2, response.context['projects'])


    def test_user_two_get_projects_public_using_HTMX(self):
        """user two can sucefully requests the projects_public view
        response contains only the public projects
        the response is a partial html"""
        
        response = self.client.get(self.routes['public'], **self.use_HTMX)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/snippets/project_list.html')
        self.assertNotIn('progress/base.html', response.templates)

        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])

  

    ### PROJECTS ALL VIEW
    def test_user_anonimous_get_projects_all(self):
        """anonimous user can requests the projects_all view
        response contains only the public projects"""
        
        response = self.client.get(self.routes['all'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])



    def test_user_anonimous_get_projects_all_using_HTMX(self):
        """anonimous user can sucefully requests the projects_all view
        response contains only the public projects
        the response is a partial html"""
        
        response = self.client.get(self.routes['all'], **self.use_HTMX)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/snippets/project_list.html')
        self.assertNotIn('progress/base.html', response.templates)

        self.assertIn(self.public_project_1, response.context['projects'])
        self.assertNotIn(self.private_project_1, response.context['projects'])


    def test_user_one_get_get_projects_all(self):
        """user one can sucefully requests the projects_all view
        response contains private user one project and all public projects"""

        self.client.force_login(self.user_one)
        response = self.client.get(self.routes['all'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])

        # it's also present the private project of the current user
        self.assertIn(self.private_project_1, response.context['projects'])

        # user cannot see private projects of other users
        self.assertNotIn(self.private_project_2, response.context['projects'])


    def test_user_one_get_get_projects_all(self):
        """user one can sucefully requests the projects_all view
        response contains private user one project and all public projects"""

        self.client.force_login(self.user_one)
        response = self.client.get(self.routes['all'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/project_list.html')
        self.assertIn(self.public_project_1, response.context['projects'])

        # it's also present the private project of the current user
        self.assertIn(self.private_project_1, response.context['projects'])

        # user cannot see private projects of other users
        self.assertNotIn(self.private_project_2, response.context['projects'])


    # ADMIN PROJECT VIEW
    def test_not_staff_users_cannot_request_suceffully_admin_view(self):
        """user with no staff permition cannot accesss to admin_project_view"""

        # User One
        self.client.force_login(self.user_one)
        response = self.client.get(self.routes['admin_view'])

        self.assertNotEqual(response.status_code, 200)
        self.assertIsNone(response.context)
        self.assertEqual(response.content, b'')

        # User Two
        self.client.force_login(self.user_two)
        response = self.client.get(self.routes['admin_view'])

        self.assertNotEqual(response.status_code, 200)
        self.assertIsNone(response.context)
        self.assertEqual(response.content, b'')

    def test_superuser_can_access_admin_view(self):
        """admin_user is superuser so it can access to admin_project_view"""

        self.client.force_login(self.user_admin)
        response = self.client.get(self.routes['admin_view'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.private_project_1, response.context['project'])


    def test_detail_project_view_protects_private_projects(self):
        """users cannot access to detail project view of private projects 
            from another users"""
        
        # user one is not the owner of this project
        self.client.force_login(self.user_one)
        response = self.client.get(self.routes['detail_private_2'])

        self.assertEqual(response.status_code, 403)

        # user two is the owner
        self.client.force_login(self.user_two)
        response = self.client.get(self.routes['detail_private_2'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.private_project_2, response.context['project'])

