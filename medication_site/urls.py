"""Корневая маршрутизация веб-интерфейса."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("medicines/", include("medicines.urls")),
    path("schedules/", include("schedules.urls")),
    path("intakes/", include("intakes.urls")),
]

if getattr(settings, "DEBUG_TOOLBAR_AVAILABLE", False):
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

handler404 = "homepage.views.page_not_found"
