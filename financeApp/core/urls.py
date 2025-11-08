from django.urls import path

from .views import KonsultasiyaCreateView, home

urlpatterns = [
    path("", home, name="home"),
    path("konsultasiya/gonder/", KonsultasiyaCreateView.as_view(), name="konsultasiya_gonder"),
]
