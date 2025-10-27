from django.shortcuts import render


def register_choice(request):
    """Display the registration type selection page."""
    return render(request, "accounts/register_choice.html")


def register_sahibkar(request):
    """Placeholder page for the entrepreneur registration form."""
    return render(request, "accounts/register_sahibkar.html")


def register_isci(request):
    """Placeholder page for the worker registration form."""
    return render(request, "accounts/register_isci.html")
