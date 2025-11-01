from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm # Django-nun hazır login forması
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import OwnerRegistrationForm, WorkerRegistrationForm
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
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Məlumatlarınız uğurla göndərildi. Tezliklə sizinlə əlaqə saxlanılacaq.",
            )
            return redirect(reverse("worker-thanks"))
        messages.error(request, "Zəhmət olmasa formdakı səhvləri düzəldin.")
    else:
        form = WorkerRegistrationForm()

    return render(
        request,
        "accounts/worker_register.html",
        {
            "form": form,
        },
    )


def register_owner(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            _notify_admin(registration)
            messages.success(request, "Qeydiyyatınız tamamlandı.")
            return redirect("home")
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


def worker_thanks(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/worker_thanks.html")


def login_view(request: HttpRequest) -> HttpResponse:
    """
    İstifadəçi giriş səhifəsi (Sahibkar və İşçi üçün ortaq)
    """
    if request.user.is_authenticated:
        # Əgər artıq daxil olubsa, birbaşa dashboard-a yönləndir
        # HƏLƏLİK dashboard səhifəmiz yoxdur, ona görə ana səhifəyə yönləndiririk
        # return redirect('owner_dashboard') # Gələcəkdə belə olacaq
        return redirect('/')  # Hələlik ana səhifəyə

    if request.method == "POST":
        # Django-nun daxili AuthenticationForm-u istifadə edirik.
        # Bu forma "username" (biz email istifadə edirik) və "password" sahələrini yoxlayır.
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Məlumatlar düzgündürsə...
            username = form.cleaned_data.get('username')  # Bu, bizim 'email' sahəmizdir
            password = form.cleaned_data.get('password')

            # İstifadəçini yoxla
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # İstifadəçi varsa və şifrə düzdürsə, sessiyaya daxil et
                login(request, user)

                # TODO: İstifadəçinin Sahibkar yoxsa İşçi olduğunu yoxlayıb
                # müvafiq panelə yönləndirmək lazımdır.
                # Hələlik ana səhifəyə yönləndiririk.
                messages.success(request, f"Xoş gəldiniz, {user.first_name}!")

                # GƏLƏCƏKDƏ:
                # try:
                #    if request.user.ownerregistration:
                #        return redirect('owner_dashboard')
                # except:
                #    pass # və ya worker_dashboard-a yönləndir

                return redirect('/')
            else:
                # İstifadəçi yoxdursa və ya şifrə səhvdirsə
                messages.error(request, "E-poçt və ya şifrə yanlışdır.")
        else:
            # Form düzgün doldurulmayıbsa
            messages.error(request, "E-poçt və ya şifrə yanlışdır.")

    else:
        # GET sorğusu olarsa, boş login forması göstər
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    İstifadəçi çıxış funksiyası
    """
    logout(request)
    messages.info(request, "Hesabınızdan uğurla çıxış etdiniz.")
    return redirect('login')  # Çıxışdan sonra login səhifəsinə yönləndir