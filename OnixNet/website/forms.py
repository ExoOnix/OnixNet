from django import forms
from .models import Community

class UploadForm(forms.Form):
    community = forms.ModelChoiceField(
        queryset=Community.objects.all().distinct(),
        widget=forms.Select(),
        required=True,
    )
    title = forms.CharField(label="Title", max_length=200, required=True)
    content = forms.CharField(widget=forms.Textarea(), required=True)

class CommentForm(forms.Form):
    content = forms.CharField(label="", required=True)

class CommunityCreateForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, min_length=2, required=True)
    description = forms.CharField(label="Description", max_length=600, required=True)