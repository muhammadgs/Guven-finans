# Generated manually because Django management commands are unavailable in this environment.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_workerregistration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workerregistration",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
