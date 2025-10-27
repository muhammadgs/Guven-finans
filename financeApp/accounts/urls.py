from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.register_choice, name="register_choice"),
    path("sahibkar/", views.register_sahibkar, name="register_sahibkar"),
    path("isci/", views.register_isci, name="register_isci"),
]
