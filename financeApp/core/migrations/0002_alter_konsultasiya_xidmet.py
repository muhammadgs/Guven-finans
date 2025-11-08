from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="konsultasiya",
            name="xidmet",
            field=models.CharField(
                choices=[
                    ("MUHASIBAT", "Mühasibatlıq"),
                    ("VERGI", "Vergi"),
                    ("IKT", "İKT"),
                    ("INSAN_RESURSLARI", "İnsan Resursları"),
                    ("HUQUQI", "Hüquqi"),
                ],
                max_length=20,
            ),
        ),
    ]
