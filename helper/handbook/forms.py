import json

from django import forms
from .models import Comment, Monster


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Оставьте комментарий...',
                'class': 'form-control'
            }),
        }

