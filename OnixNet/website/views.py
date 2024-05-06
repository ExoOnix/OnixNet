from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Community, Comment, Reply

from .forms import UploadForm

class index(ListView):
    model = Post
    paginate_by = 100
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

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
        context["comments"] = Comment.objects.filter(post__pk=self.kwargs["pk"])
        context["replys"] = Reply.objects.filter(comment__pk=self.kwargs["pk"])
        return context

def Upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST)
        if form.is_valid():

            print(form.cleaned_data)
            post_instance = Post(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author=request.user,
                community=Community.objects.get(id=form.cleaned_data["community"].id),
            )
            post_instance.save()
            return HttpResponseRedirect(f"/c/{Community.objects.get(id=form.cleaned_data['community'].id).name}/{post_instance.pk}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": UploadForm})
