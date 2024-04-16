# Generated by Django 5.0.4 on 2024-04-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='audio_files')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]