from django.urls import path

from .views import CardView


urlpatterns = [
    path('card/<str:pk>', CardView.as_view(), name='card'),
]