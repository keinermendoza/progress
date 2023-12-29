from django.test import TestCase
from django.urls import reverse, resolve
from progress.views import projects_home, projects_all, project_detail\
, projects_private, projects_public, admin_project_view

class TestProgressUrls(TestCase):
    """reverse names call the respectives functions"""
    
    def test_home_url(self):
        url = reverse('progress:projects_home')
        self.assertEquals(resolve(url).func, projects_home)

    def test_projects_all_url(self):
        url = reverse('progress:projects_all')
        self.assertEquals(resolve(url).func, projects_all)

    def test_projects_public_url(self):
        url = reverse('progress:projects_public')
        self.assertEquals(resolve(url).func, projects_public)

    def test_projects_private_url(self):
        url = reverse('progress:projects_private')
        self.assertEquals(resolve(url).func, projects_private)

    def test_project_detail_url(self):
        url = reverse('progress:project_detail', args=[123456789])
        self.assertEquals(resolve(url).func, project_detail)

    def test_admin_project_view_url(self):
        url = reverse('progress:admin_project_view', args=[123456789])
        self.assertEquals(resolve(url).func, admin_project_view)

