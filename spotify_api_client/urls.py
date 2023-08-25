from django.urls import path
from .views import GetNewReleases

urlpatterns = [
    path('new_release/', GetNewReleases.as_view(), name='spotify-new_release'),
]
