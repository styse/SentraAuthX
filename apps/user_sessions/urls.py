from django.urls import path
from .views import (
    UserSessionListView, UserSessionDeleteView
)

urlpatterns = [
    path("list/", UserSessionListView.as_view(), name = 'user-session-list'),
    path("delete/<uuid:session_id>", UserSessionDeleteView.as_view(), name= 'user-session-delete'),
]
