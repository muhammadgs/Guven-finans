from django.contrib import admin

from .models import Konsultasiya


@admin.register(Konsultasiya)
class KonsultasiyaAdmin(admin.ModelAdmin):
    list_display = ("ad_sirket", "elaqe_nomresi", "xidmet", "created_at")
    list_filter = ("xidmet", "created_at")
    search_fields = ("ad_sirket", "elaqe_nomresi", "etrafli")
