from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()

class Community(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="communities", blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    vote = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="children")
    created_at = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(User, related_name="comment_upvotes", blank=True)
    downvote = models.ManyToManyField(User, related_name="comment_downvotes", blank=True)
    @property
    def upvotes_count(self):
        return self.upvote.count() - self.downvote.count()
    def __str__(self):
        return str(self.upvote.count() - self.downvote.count())


class Attachment(models.Model):
    image = models.ImageField(upload_to="attachments/", null=True, default=None)
    video = models.FileField(upload_to="attachments/", null=True, default=None)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")

    def clean(self):
        if self.video and self.image:
            raise ValidationError("Please select only a video OR an image, not both.")
    def __str__(self):
        return str(self.parent_post)
