from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from .models import Post, Community, Comment


from .forms import UploadForm, CommentForm, CommunityCreateForm

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


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = "post_detail.html"
    form_class = CommentForm
    def get_success_url(self):
        return redirect(".")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        context["comments"] = Comment.objects.filter(parent_post__pk=self.kwargs["pk"]).order_by('-created_at')
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        print(form.cleaned_data)
        comment_instance = Comment(
            content=form.cleaned_data["content"],
            author=self.request.user,
            parent_post=Post.objects.get(pk=self.kwargs['pk']),
        )
        
        comment_instance.save()
        return HttpResponseRedirect(
            f"/c/{self.kwargs['community']}/{self.kwargs['pk']}"
        )
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

def CreateCommunity(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)

        if form.is_valid():
            if not Community.objects.filter(name=form.cleaned_data["name"]).exists():
                community_instance = Community(
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    admin=request.user,
                )
                community_instance.save()
                return HttpResponseRedirect(
                    f"/c/{form.cleaned_data['name']}"
                )

    else:
        form = CommunityCreateForm()
    return render(request, "create-community.html", {"form": CommunityCreateForm})
