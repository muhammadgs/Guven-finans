from django.db import models


class Konsultasiya(models.Model):
    class Xidmetler(models.TextChoices):
        MUHASIBAT = "MUHASIBAT", "Mühasibatlıq xidmətləri"
        VERGI = "VERGI", "Vergi xidmətləri"
        IKT = "IKT", "İKT"
        INSAN_RESURS = "INSAN_RESURS", "İnsan Resursları"
        HUQUQI = "HUQUQI", "Hüquqi xidmətlərin təsviri"

    ad_sirket = models.CharField(max_length=255)
    elaqe_nomresi = models.CharField(max_length=20)
    xidmet = models.CharField(max_length=20, choices=Xidmetler.choices)
    etrafli = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.ad_sirket} ({self.get_xidmet_display()})"
