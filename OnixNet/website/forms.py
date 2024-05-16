from django import forms
from .models import Community

# Multi file uploads


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadForm(forms.Form):
    # community = forms.ModelChoiceField(
    #    queryset=Community.objects.all(),
    #    widget=forms.Select(),
    #    required=True,
    # )
    title = forms.CharField(label="Title", max_length=200, required=True)
    content = forms.CharField(widget=forms.Textarea(), required=True)
    attachments = MultipleFileField(required=False)


class CommentForm(forms.Form):
    content = forms.CharField(label="", required=True)

class CommunityCreateForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, min_length=2, required=True)
    description = forms.CharField(label="Description", max_length=600, required=True)
