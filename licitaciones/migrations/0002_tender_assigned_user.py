# Generated by Django 4.2 on 2024-06-05 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('licitaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='assigned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tenders', to=settings.AUTH_USER_MODEL),
        ),
    ]
