from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .recommend import Recommend

import filetype

# Reccomendations
import pandas as pd
import numpy as np
import scipy.stats

from .models import Post, Community, Comment, Attachment, Reaction
from .forms import UploadForm, CommentForm, CommunityCreateForm


recommend = Recommend()
recommend.Update()
# print(recommend.Recommend(1))
class index(ListView):
    model = Post
    paginate_by = 100
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            object_list = Post.objects.filter(title__icontains=search).order_by('-created_at')
        else:
            if self.request.user.is_authenticated:
                # Fetch recommendations for the authenticated user
                try:
                    rec_list = recommend.Recommend(self.request.user.pk).values.tolist()
                    # Extract post IDs from the recommendation list
                    recommended_post_ids = [rec[0] for rec in rec_list]
                    # Fetch posts corresponding to recommended post IDs
                    recommended_posts = Post.objects.filter(pk__in=recommended_post_ids)
                    # Extract remaining post IDs not in the recommendation list
                    remaining_post_ids = [post.id for post in Post.objects.exclude(pk__in=recommended_post_ids)]
                    # Fetch remaining posts
                    remaining_posts = Post.objects.filter(pk__in=remaining_post_ids)

                    # Concatenate recommended posts and remaining posts
                    recommended_posts_list = list(recommended_posts)
                    remaining_posts_list = list(remaining_posts.order_by('-created_at'))
                    print(recommended_posts_list, remaining_posts_list)
                    object_list = recommended_posts_list + remaining_posts_list
                    # object_list = recommended_posts.union(remaining_posts, all=True)
                except:
                    object_list = Post.objects.all().order_by("-created_at")
            else:
                object_list = Post.objects.all().order_by("-created_at")
        return object_list

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
        context["upvotes"] = Reaction.objects.filter(parent_post=self.kwargs["pk"], vote=True)
        context["downvotes"] = Reaction.objects.filter(parent_post=self.kwargs["pk"], vote=False)
        if self.request.user.is_authenticated:
            context["is_upvote"] = Reaction.objects.filter(parent_post=self.kwargs["pk"], vote=True, user=self.request.user)
            context["is_downvote"] = Reaction.objects.filter(parent_post=self.kwargs["pk"], vote=False, user=self.request.user)

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
    if request.user.is_authenticated:
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
                            recommend.Update()
                return HttpResponseRedirect(f"/c/{Community.objects.get(id=int(request.POST.get('community'))).name}/{post_instance.pk}")

        # if a GET (or any other method) we'll create a blank form
        else:
            form = UploadForm()
        return render(request, "upload.html", {"form": UploadForm, "communities": request.user.communities.all()})
    else:
        raise PermissionDenied
def CreateCommunity(request):
    if request.user.is_authenticated:
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
    else:
        raise PermissionDenied

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
        raise PermissionDenied


def DeleteComment(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.pk == Comment.objects.get(pk=kwargs["pk"]).author.pk or request.user.is_superuser == True:
            Comment.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/c/{kwargs['community']}/{kwargs['post_pk']}")
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def DeletePost(request, **kwargs):
    if request.user.is_authenticated:
        if (
            request.user.pk == Post.objects.get(pk=kwargs["pk"]).author.pk
            or request.user.is_superuser == True
        ):
            Post.objects.get(pk=kwargs["pk"]).delete()
            return redirect(f"/c/{kwargs['community']}")
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def JoinCommunity(request, **kwargs):
    if request.user.is_authenticated:
        community = Community.objects.get(name=kwargs["community"])
        community.members.add(request.user)
        community.save()
        return redirect(f"/c/{kwargs['community']}")
    else:
        raise PermissionDenied


def LeaveCommunity(request, **kwargs):
    if request.user.is_authenticated:
        community = Community.objects.get(name=kwargs["community"])
        community.members.remove(request.user)
        community.save()
        return redirect(f"/c/{kwargs['community']}")
    else:
        raise PermissionDenied


def UpvotePost(request, **kwargs):
    if request.user.is_authenticated:
        reaction = Reaction.objects.filter(
            parent_post=kwargs["pk"], user=request.user
        )
        if len(reaction) > 0:
            reaction.delete()
        else:
            reaction = Reaction(
                user=request.user,
                parent_post=Post.objects.get(pk=kwargs["pk"]),
                vote=True
            )
            reaction.save()
        return redirect(f"/c/{kwargs['community']}/{kwargs['pk']}")
    else:
        raise PermissionDenied

def DownvotePost(request, **kwargs):
    if request.user.is_authenticated:
        reaction = Reaction.objects.filter(
            parent_post=kwargs["pk"], user=request.user
        )
        if len(reaction) > 0:
            reaction.delete()
        else:
            reaction = Reaction(
                user=request.user,
                parent_post=Post.objects.get(pk=kwargs["pk"]),
                vote=False
            )
            reaction.save()
        return redirect(f"/c/{kwargs['community']}/{kwargs['pk']}")
    else:
        raise PermissionDenied


def UpvoteComment(request, **kwargs):
    if request.user.is_authenticated:
        if not request.user.comment_downvotes.filter(pk=kwargs["pk"]).exists():

            if request.user.comment_upvotes.filter(pk=kwargs["pk"]).exists():
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.upvote.remove(request.user)
                comment.save()
            else:
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.upvote.add(request.user)
                comment.save()
        return redirect(f"/c/{kwargs['community']}/{kwargs['post_pk']}")
    else:
        raise PermissionDenied


def DownvoteComment(request, **kwargs):
    if request.user.is_authenticated:
        if not request.user.comment_upvotes.filter(pk=kwargs["pk"]).exists():
            if request.user.comment_downvotes.filter(pk=kwargs["pk"]).exists():
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.downvote.remove(request.user)
                comment.save()
            else:
                comment = Comment.objects.get(pk=kwargs["pk"])
                comment.downvote.add(request.user)
                comment.save()
        return redirect(f"/c/{kwargs['community']}/{kwargs['post_pk']}")
    else:
        raise PermissionDenied
