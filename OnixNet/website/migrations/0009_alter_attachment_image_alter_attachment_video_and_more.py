# Generated by Django 4.2.11 on 2024-05-09 12:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0008_alter_community_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='video',
            field=models.FileField(default=None, null=True, upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='communities', to=settings.AUTH_USER_MODEL),
        ),
    ]
