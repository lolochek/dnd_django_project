from django import forms
from .models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'login', 'profile_description', 'avatar']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(username=login).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return login
