from django.urls import path
from .views import (
    UserSessionListView
)

urlpatterns = [
    path("list/", UserSessionListView.as_view(), name = 'user-session-list'),
]
