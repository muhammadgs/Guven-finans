from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Konsultasiya",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ad_sirket", models.CharField(max_length=255)),
                ("elaqe_nomresi", models.CharField(max_length=20)),
                (
                    "xidmet",
                    models.CharField(
                        choices=[
                            ("MUHASIBAT", "Mühasibatlıq xidmətləri"),
                            ("VERGI", "Vergi xidmətləri"),
                            ("IKT", "İKT"),
                            ("INSAN_RESURS", "İnsan Resursları"),
                            ("HUQUQI", "Hüquqi xidmətlərin təsviri"),
                        ],
                        max_length=20,
                    ),
                ),
                ("etrafli", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]

