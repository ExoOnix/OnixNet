from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post

class index(ListView):
    model = Post
    paginate_by = 100
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
