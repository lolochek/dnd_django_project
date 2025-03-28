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

class MonsterEditForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    hit_points = forms.IntegerField(required=False)
    armor_class = forms.IntegerField(required=False)
    speed = forms.CharField(max_length=100, required=False)
    abilities = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="JSON формат или оставьте пустым"
    )
    additional_info = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="JSON формат или оставьте пустым"
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description
            self.fields['hit_points'].initial = instance.hit_points
            self.fields['armor_class'].initial = instance.armor_class
            self.fields['speed'].initial = instance.speed

            self.fields['abilities'].initial = json.dumps(instance.abilities, ensure_ascii=False, indent=2) if instance.abilities else '{}'
            self.fields['additional_info'].initial = json.dumps(instance.additional_info, ensure_ascii=False, indent=2) if instance.additional_info else '{}'

    def clean_abilities(self):
        data = self.cleaned_data.get('abilities', '').strip()
        if not data:
            return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Поле abilities должно содержать корректный JSON.')

    def clean_additional_info(self):
        data = self.cleaned_data.get('additional_info', '').strip()
        if not data:
            return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Поле additional_info должно содержать корректный JSON.')
