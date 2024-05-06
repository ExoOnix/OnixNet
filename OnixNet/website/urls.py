from django.urls import path
from .views import index, PostDetailView, CommunityView

from . import views

urlpatterns = [
    path("", index.as_view(), name="index"),
    path("<str:community>", CommunityView.as_view(), name="community"),
    path("<str:community>/<int:pk>/", PostDetailView.as_view(), name="article-detail"),
]
