from django.contrib import admin

from .models import OwnerRegistration


@admin.register(OwnerRegistration)
class OwnerRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "company_name",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "first_name",
        "last_name",
        "company_name",
        "email",
        "company_email",
    )
    ordering = ("-created_at",)
