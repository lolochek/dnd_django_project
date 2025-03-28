from django import forms
from .models import Article
from profiles.models import User

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class ArticleSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Поиск по названию или контенту',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по статье...'})
    )
    author = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.all(),
        label="Автор",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выберите автора"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].queryset = User.objects.filter(is_staff=False)
        self.fields['author'].label_from_instance = lambda obj: obj.login
