from django.urls import path

from .views import LoginView, logout_view


app_name='auths'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
]