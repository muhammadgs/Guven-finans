from django.urls import path
from . import views

urlpatterns = [
    # Şablonların tələb etdiyi adlar (tire ilə):
    path('choice/', views.register_choice, name='register-choice'),
    path('owner/', views.register_owner, name='register-owner'),
    path('worker/', views.register_worker, name='register-worker'),

    # Bunlar hələlik belə qala bilər (views.py-dən yönlənir)
    path('owner/thanks/', views.owner_thanks, name='owner-thanks'),
    path('worker/thanks/', views.worker_thanks, name='worker-thanks'),

    # Login / Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]