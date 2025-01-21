from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Image, Post, Tag, Registr, Profile, Author


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

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=8)
    class Meta:
        model = Registr
        fields = ['name', 'email', 'password', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create(
            username=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password']),
        )
        profile = Profile.objects.create(
            user=user,
            avatar=self.cleaned_data['avatar']
        )

        registr = super().save(commit=False)
        registr.user = user
        registr.save()
        return registr

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'image']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            print(f"Processed tags{tag_list}")
            tag_objects = []
            for tag_name in tag_list:
                if not tag_name:
                    continue
                try:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag)
                except Exception as e:
                    raise ValidationError(f"Invalid tag {tag_name}. Error: {e}")
            return tag_objects
        return []

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()

        tags = self.cleaned_data['tags']
        post.tags.set(tags)
        return post

