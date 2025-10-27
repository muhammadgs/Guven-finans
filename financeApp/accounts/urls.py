from django.urls import path

from . import views


urlpatterns = [
    path("qeydiyyat/", views.register_choice, name="register-choice"),
    path("qeydiyyat/sahibkar/", views.register_owner, name="register-owner"),
    path(
        "qeydiyyat/sahibkar/təşəkkürlər/",
        views.owner_thanks,
        name="owner-thanks",
    ),
    path("qeydiyyat/isci/", views.register_worker, name="register-worker"),
]
