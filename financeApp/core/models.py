from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.ImageField(upload_to="projects/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Konsultasiya(models.Model):
    class Xidmetler(models.TextChoices):
        MUHASIBAT = "MUHASIBAT", "Mühasibatlıq"
        VERGI = "VERGI", "Vergi"
        IKT = "IKT", "İKT"
        INSAN_RESURSLARI = "INSAN_RESURSLARI", "İnsan Resursları"
        HUQUQI = "HUQUQI", "Hüquqi"

    ad_sirket = models.CharField(max_length=255)
    elaqe_nomresi = models.CharField(max_length=20)
    xidmet = models.CharField(max_length=20, choices=Xidmetler.choices)
    etrafli = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.ad_sirket} ({self.get_xidmet_display()})"
