from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from typing import Optional

from .forms import EmployeeForm, OwnerRegistrationForm, UserLoginForm, WorkerRegistrationForm
from .cache_utils import clear_user_runtime_state
from .models import OwnerRegistration, WorkerRegistration


def _get_owner_profile(user) -> Optional[OwnerRegistration]:
    if not user.is_authenticated:
        return None

    try:
        owner_profile = user.ownerregistration
        if owner_profile:
            return owner_profile
    except OwnerRegistration.DoesNotExist:
        pass

    if user.email:
        return OwnerRegistration.objects.filter(email=user.email).first()
    return OwnerRegistration.objects.filter(user=user).first()


def _get_worker_profile(user) -> Optional[WorkerRegistration]:
    if not user.is_authenticated:
        return None

    try:
        worker_profile = user.workerregistration
        if worker_profile:
            return worker_profile
    except WorkerRegistration.DoesNotExist:
        pass

    if user.email:
        worker_profile = WorkerRegistration.objects.filter(email=user.email).first()
        if worker_profile:
            return worker_profile
    return WorkerRegistration.objects.filter(user=user).first()


def _resolve_dashboard_url_name(user) -> str:
    if _get_worker_profile(user):
        return "worker-dashboard"
    if _get_owner_profile(user):
        return "owner-dashboard"
    return "owner-dashboard"


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


def isci_qeydiyyat(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Qeydiyyat tamamlandi.")
            return redirect("home")
    else:
        form = EmployeeForm()

    return render(request, "accounts/isci_form.html", {"form": form})


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


@login_required
def owner_dashboard(request: HttpRequest) -> HttpResponse:
    owner_profile = _get_owner_profile(request.user)

    company_name = owner_profile.company_name if owner_profile and owner_profile.company_name else "Biznesiniz"
    display_name = request.user.get_full_name() or request.user.username
    initials = "".join(part[0] for part in display_name.split() if part).upper()
    if not initials:
        initials = (request.user.username[:2] or "SP").upper()

    context = {
        "company_name": company_name,
        "owner_display_name": display_name,
        "owner_initials": initials[:2],
        "owner_role_label": "Sahibkar",
    }
    return render(request, "accounts/owner_dashboard.html", context)


@login_required
def worker_dashboard(request: HttpRequest) -> HttpResponse:
    worker_profile = _get_worker_profile(request.user)
    if worker_profile is None:
        return redirect("owner-dashboard")

    display_name = (request.user.get_full_name() or "").strip()
    if not display_name and worker_profile:
        display_name = f"{worker_profile.first_name} {worker_profile.last_name}".strip()
    if not display_name:
        display_name = request.user.username or worker_profile.email

    initials = "".join(part[0] for part in display_name.split() if part).upper()
    if not initials:
        initials = (request.user.username[:2] or "IW").upper()

    context = {
        "worker_display_name": display_name,
        "worker_initials": initials[:2],
        "worker_role_label": "İşçi",
    }
    return render(request, "accounts/worker_dashboard.html", context)


def login_view(request: HttpRequest) -> HttpResponse:
    """
    İstifadəçi giriş səhifəsi (Sahibkar və İşçi üçün ortaq)
    """
    if request.user.is_authenticated:
        return redirect(_resolve_dashboard_url_name(request.user))

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

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
                # GƏLƏCƏKDƏ:
                # try:
                #    if request.user.ownerregistration:
                #        return redirect('owner_dashboard')
                # except:
                #    pass # və ya worker_dashboard-a yönləndir

                return redirect(_resolve_dashboard_url_name(user))
            else:
                # İstifadəçi yoxdursa və ya şifrə səhvdirsə
                messages.error(request, "E-poçt və ya şifrə yanlışdır.")
        else:
            # Form düzgün doldurulmayıbsa
            messages.error(request, "E-poçt və ya şifrə yanlışdır.")

    else:
        # GET sorğusu olarsa, boş login forması göstər
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    İstifadəçi çıxış funksiyası
    """
    logout(request)
    messages.info(request, "Hesabınızdan uğurla çıxış etdiniz.")
    return redirect('login')  # Çıxışdan sonra login səhifəsinə yönləndir


@csrf_exempt
@login_required
@require_POST
def clear_user_cache(request: HttpRequest) -> JsonResponse:
    """Endpoint to clear cached/session data when the tab closes."""

    clear_user_runtime_state(request.user, session=request.session)
    return JsonResponse({"status": "cleared"})

