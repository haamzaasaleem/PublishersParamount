# Generated by Django 4.1.2 on 2022-10-15 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='journals', to=settings.AUTH_USER_MODEL),
        ),
    ]
