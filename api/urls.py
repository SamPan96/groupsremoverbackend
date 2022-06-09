from django.urls import path

from .views import RemoveGroups

urlpatterns = [
    path('removegroups', RemoveGroups.as_view()),
]
