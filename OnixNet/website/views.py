from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
import filetype

from .models import Post, Community, Comment, Attachment
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
        return Post.objects.filter(community__name=self.kwargs["community"]).order_by('-created_at')


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
        form = UploadForm(request.POST, request.FILES)
        print(form.errors.as_text)
        if form.is_valid():
            post_instance = Post(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author=request.user,
                community=Community.objects.get(id=int(request.POST.get("community"))),
            )
            post_instance.save()
            print("cleaned data", form.cleaned_data)

            if len(form.cleaned_data["attachments"]) > 0:
                files = form.cleaned_data["attachments"]
                for f in files:
                    if "image" in filetype.guess(f).mime:
                        attachment_instance = Attachment(
                            parent_post=post_instance,
                            image=f
                        )
                        attachment_instance.save()
                    if "video" in filetype.guess(f).mime:
                        attachment_instance = Attachment(
                            parent_post=post_instance,
                            video=f
                        )
                        attachment_instance.save()
            return HttpResponseRedirect(f"/c/{Community.objects.get(id=int(request.POST.get('community'))).name}/{post_instance.pk}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": UploadForm, "communities": request.user.communities.all()})

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
                community_instance.members.add(request.user)
                community_instance.save()

                return HttpResponseRedirect(
                    f"/c/{form.cleaned_data['name']}"
                )

    else:
        form = CommunityCreateForm()
    return render(request, "create-community.html", {"form": CommunityCreateForm})

def Reply(request, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            
            if form.is_valid():
                print(form.cleaned_data, kwargs["community"], kwargs["post_pk"], kwargs["pk"])
                comment_instance = Comment(
                    content=form.cleaned_data["content"],
                    author=request.user,
                    parent_post=Post.objects.get(pk=kwargs['post_pk']),
                    parent_comment=Comment.objects.get(pk=kwargs["pk"]),
                )
                
                comment_instance.save()
                return redirect(
                    f"/c/{kwargs['community']}/{kwargs['post_pk']}"
                )
        else:
            redirect("/")
    else:
        return redirect("/")

def DeleteComment(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.pk == Comment.objects.get(pk=kwargs["pk"]).author.pk or request.user.is_superuser == True:
            Comment.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/c/{kwargs['community']}/{kwargs['post_pk']}")
        else:
            return HttpResponse("Not allowed")
    else:
        return HttpResponse("Not allowed")


def DeletePost(request, **kwargs):
    if request.user.is_authenticated:
        if (
            request.user.pk == Post.objects.get(pk=kwargs["pk"]).author.pk
            or request.user.is_superuser == True
        ):
            Post.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/c/{kwargs['community']}")
        else:
            return HttpResponse("Not allowed")
    else:
        return HttpResponse("Not allowed")


def JoinCommunity(request, **kwargs):
    if request.user.is_authenticated:
        community = Community.objects.get(name=kwargs["community"])
        community.members.add(request.user)
        community.save()
        return redirect(f"/c/{kwargs['community']}")
    else:
        return HttpResponse("Not allowed")


def LeaveCommunity(request, **kwargs):
    if request.user.is_authenticated:
        community = Community.objects.get(name=kwargs["community"])
        community.members.remove(request.user)
        community.save()
        return redirect(f"/c/{kwargs['community']}")
    else:
        return HttpResponse("Not allowed")
