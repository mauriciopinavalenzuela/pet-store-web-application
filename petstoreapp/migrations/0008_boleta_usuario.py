# Generated by Django 4.1 on 2023-07-12 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petstoreapp', '0007_boleta_impuesto_alter_seguimientoorden_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleta',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]