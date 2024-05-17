from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, PostDetailView, CommunityView

from . import views


urlpatterns = [
    path("", index.as_view(), name="index"),
    path("upload", views.Upload, name="upload"),
    path("createcommunity", views.CreateCommunity, name="create-community"),
    path("c/<str:community>", CommunityView.as_view(), name="community"),
    path("c/<str:community>/join", views.JoinCommunity, name="join-community"),
    path("c/<str:community>/leave", views.LeaveCommunity, name="leave-community"),
    path("c/<str:community>/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("c/<str:community>/<int:pk>/upvote", views.UpvotePost, name="upvote-post"),
    path("c/<str:community>/<int:pk>/downvote", views.DownvotePost, name="downvote-post"),
    path("c/<str:community>/<str:post_pk>/upvote/<int:pk>", views.UpvoteComment, name="upvote-comment"),
    path("c/<str:community>/<str:post_pk>/downvote/<int:pk>", views.DownvoteComment, name="downvote-post"),
    path("c/<str:community>/<str:post_pk>/reply/<int:pk>", views.Reply, name="reply"),
    path(
        "c/<str:community>/<str:post_pk>/delete/<int:pk>",
        views.DeleteComment,
        name="delete",
    ),
    path("c/<str:community>/<int:pk>/delete", views.DeletePost, name="delete-post"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
