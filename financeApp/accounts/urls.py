from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("qeydiyyat/sahibkar/", views.register_owner, name="register-owner"),
    path(
        "qeydiyyat/sahibkar/təşəkkürlər/",
        views.owner_thanks,
        name="owner-thanks",
    ),
]
