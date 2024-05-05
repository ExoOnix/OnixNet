from django.urls import path
from .views import index, PostDetailView

from . import views

urlpatterns = [
    path("", index.as_view(), name="index"),
    path("<str:community>/<int:pk>/", PostDetailView.as_view(), name="article-detail"),
]
