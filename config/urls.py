from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    # schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # swagger UI
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # redoc UI
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-ui",
    ),

    # admin
    path("admin/", admin.site.urls),

    # apps
    path('api/users/', include('apps.users.urls')),
    path('api/sessions/', include('apps.user_sessions.urls'))
]
