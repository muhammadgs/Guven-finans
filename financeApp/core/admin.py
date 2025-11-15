from django.contrib import admin

from .models import Konsultasiya, Project


@admin.register(Konsultasiya)
class KonsultasiyaAdmin(admin.ModelAdmin):
    list_display = ("ad_sirket", "elaqe_nomresi", "xidmet", "created_at")
    list_filter = ("xidmet", "created_at")
    search_fields = ("ad_sirket", "elaqe_nomresi", "etrafli")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "link", "created_at")
    search_fields = ("name", "link")
