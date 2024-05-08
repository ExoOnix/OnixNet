# Generated by Django 4.2.11 on 2024-05-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_attachment_options_remove_attachment_file_and_more'),
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
    ]