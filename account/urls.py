from django.urls import path, reverse
from . import views
from django.views.generic import RedirectView

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('register/', views.register_view, name="register_view"),
    path('logout/', views.logout_view, name="logout_view"),


    # path('', RedirectView.as_view(url=(reverse('progress:home'))))
]
