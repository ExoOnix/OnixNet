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
    content = forms.CharField(required=True)