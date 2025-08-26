from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView


api = [
    path("v1/", include("app.urls.v1", namespace="v1")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api)),
    path("", RedirectView.as_view(url="/api/v1/docs/swagger/", permanent=False)),
]
