import hashlib
import random

from django.contrib.auth import forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import ShopUser, ShopUserProfile
import re


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''


    def save(self, **kwargs):
        user = super(ShopUserRegisterForm, self).save()
        user.is_active = False

        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        users = ShopUser.objects.all()
        uniqueEmails = set()
        for user in users:
            uniqueEmails.add(user.__dict__['email'])
        if data in uniqueEmails and data !='':
            raise forms.ValidationError("Эта почта уже используется. Укажите другую")
        return data

    def clean_password1(self):
        data = self.cleaned_data['password1']
        match = re.search(r'[\w]{8,}', data)
        if not match:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов, а так же состоять только из букв, цифр и знака подчеркивани _")
        return data



class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''
            if filed_name == 'password':
                field.widget = forms.HiddenInput()


    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды")
        return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about_me', 'gender')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
