from django import forms
from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'textAreaComment', 'rows':"5"})}

    def __int__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
