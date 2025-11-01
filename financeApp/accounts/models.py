from django.db import models
from django.contrib.auth.models import User  # BU ƏLAVƏ EDİLDİ


# Create your models here.
class OwnerRegistration(models.Model):
    # BİR SAHİBKARIN BİR İSTİFADƏÇİ HESABI OLMALIDIR
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # BU ƏLAVƏ EDİLDİ

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    # password = models.CharField(max_length=128) # BU SƏTİR SİLİNDİ (artıq User modelindədir)

    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(unique=True)
    company_phone = models.CharField(max_length=20)
    company_address = models.TextField()

    STATUS_CHOICES = [
        ('pending', 'Gözləmədə'),
        ('approved', 'Təsdiqlənmiş'),
        ('rejected', 'Rədd edilmiş'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company_name})"


class WorkerRegistration(models.Model):
    # BİR İŞÇİNİN BİR İSTİFADƏÇİ HESABI OLMALIDIR
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # BU ƏLAVƏ EDİLDİ

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    # password = models.CharField(max_length=128) # BU SƏTİR SİLİNDİ (artıq User modelindədir)

    position = models.CharField(max_length=100)
    # Şirkətə (Owner-ə) bağlamaq üçün gələcəkdə əlavə edilə bilər
    # owner = models.ForeignKey(OwnerRegistration, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"