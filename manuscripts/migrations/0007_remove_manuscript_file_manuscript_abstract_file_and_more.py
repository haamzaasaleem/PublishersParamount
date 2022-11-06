# Generated by Django 4.1.2 on 2022-10-31 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manuscripts', '0006_manuscript_journal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manuscript',
            name='file',
        ),
        migrations.AddField(
            model_name='manuscript',
            name='abstract_file',
            field=models.FileField(blank=True, null=True, upload_to='manuscripts/abstract/'),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='cover_file',
            field=models.FileField(blank=True, null=True, upload_to='manuscripts/cover/'),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='manuscript_file',
            field=models.FileField(blank=True, null=True, upload_to='manuscripts/file/'),
        ),
        migrations.CreateModel(
            name='Figures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='manuscripts/figures')),
                ('manuscript', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manuscripts.manuscript')),
            ],
        ),
    ]
