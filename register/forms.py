from django import forms
from django.forms import HiddenInput

from .models import Post


class PostUptadeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image','text','client')
        widgets = {'client': forms.HiddenInput()}
