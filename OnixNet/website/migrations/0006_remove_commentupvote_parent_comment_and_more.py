# Generated by Django 4.2.11 on 2024-05-16 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_commentupvote_commentdownvote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentupvote',
            name='parent_comment',
        ),
        migrations.RemoveField(
            model_name='commentupvote',
            name='user',
        ),
        migrations.DeleteModel(
            name='CommentDownvote',
        ),
        migrations.DeleteModel(
            name='CommentUpvote',
        ),
    ]
