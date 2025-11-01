from django.contrib import admin
from .models import OwnerRegistration, WorkerRegistration


@admin.register(OwnerRegistration)
class OwnerRegistrationAdmin(admin.ModelAdmin):
    """
    Sahibkar qeydiyyatı üçün admin paneli.
    'status' sahəsi burada qalır.
    """
    list_display = (
        'first_name',
        'last_name',
        'company_name',
        'email',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')

    # 'user' sahəsini admin panelində sadəcə oxumaq üçün əlavə edirik
    readonly_fields = ('user',)


@admin.register(WorkerRegistration)
class WorkerRegistrationAdmin(admin.ModelAdmin):
    """
    İşçi qeydiyyatı üçün admin paneli.
    Xətaya səbəb olan 'status' sahəsi buradan çıxarıldı.
    """
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'position',
        'created_at'  # 'status' yerinə 'created_at' əlavə etdim
    )
    list_filter = ('created_at',)  # 'status' buradan çıxarıldı
    search_fields = ('first_name', 'last_name', 'email', 'position')

    # 'user' sahəsini admin panelində sadəcə oxumaq üçün əlavə edirik
    readonly_fields = ('user',)