from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Community

class index(ListView):
    model = Post
    paginate_by = 100
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class CommunityView(ListView):
    model = Post
    paginate_by = 100
    template_name = "community.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = Community.objects.filter(name=self.kwargs["community"])
        if len(community) > 0:
            context["community"] = community[0]
            context["exists"] = True
        else:
            context["exists"] = False
        return context
    def get_queryset(self):
        return Post.objects.filter(community__name=self.kwargs["community"])


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
