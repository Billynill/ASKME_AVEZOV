from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, max_length= 8)
    confirm = forms.BooleanField(widget=forms.CheckboxInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=8)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirm']:
            raise forms.ValidationError('Passwords do not match')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user