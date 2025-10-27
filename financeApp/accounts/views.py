from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import OwnerRegistrationForm
from .models import OwnerRegistration


def _notify_admin(registration: OwnerRegistration) -> None:
    recipients = [email for _, email in getattr(settings, "ADMINS", [])]
    if not recipients:
        default_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
        if default_email:
            recipients = [default_email]
    if not recipients:
        return

    subject = "Yeni sahibkar qeydiyyatı"
    message_lines = [
        "Yeni sahibkar qeydiyyatı formu göndərildi:",
        f"Ad: {registration.first_name}",
        f"Soyad: {registration.last_name}",
        f"Mobil nömrə: {registration.phone}",
        f"E-poçt: {registration.email}",
        f"Şirkət adı: {registration.company_name}",
        f"Şirkət e-poçtu: {registration.company_email}",
        f"Şirkət nömrəsi: {registration.company_phone}",
        f"Şirkət ünvanı: {registration.company_address}",
        f"Status: {registration.get_status_display()}",
    ]
    message = "\n".join(message_lines)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "no-reply@localhost"

    try:
        send_mail(subject, message, from_email, recipients)
    except (BadHeaderError, Exception):
        # Email configuration is optional; ignore failures silently.
        pass


def register_choice(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/register_choice.html")


def register_worker(request: HttpRequest) -> HttpResponse:
    return HttpResponse("İşçi qeydiyyat formu gələcək")


def register_owner(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            _notify_admin(registration)
            return redirect(reverse("owner-thanks"))
        messages.error(request, "Zəhmət olmasa formdakı səhvləri düzəldin.")
    else:
        form = OwnerRegistrationForm()

    return render(
        request,
        "accounts/owner_register.html",
        {
            "form": form,
        },
    )


def owner_thanks(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/owner_thanks.html")
