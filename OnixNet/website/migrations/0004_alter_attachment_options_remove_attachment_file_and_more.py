# Generated by Django 4.2.11 on 2024-05-08 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_attachment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={},
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='file',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='publication',
        ),
        migrations.AddField(
            model_name='attachment',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='attachments/', verbose_name='Attachment'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='parent_post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attachment',
            name='video',
            field=models.FileField(default=None, null=True, upload_to='attachments/', verbose_name='Attachment'),
        ),
    ]