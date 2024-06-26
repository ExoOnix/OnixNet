# Generated by Django 4.2.11 on 2024-05-16 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_commentreaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='parent_comment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='website.comment'),
        ),
        migrations.DeleteModel(
            name='CommentReaction',
        ),
    ]
