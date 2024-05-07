from django.urls import path
from .views import index, PostDetailView, CommunityView

from . import views

urlpatterns = [
    path("", index.as_view(), name="index"),
    path("upload", views.Upload, name="upload"),
    path("createcommunity", views.CreateCommunity, name="create-community"),
    path("c/<str:community>", CommunityView.as_view(), name="community"),
    path("c/<str:community>/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("c/<str:community>/<str:post_pk>/reply/<int:pk>", views.Reply, name="reply"),
]
