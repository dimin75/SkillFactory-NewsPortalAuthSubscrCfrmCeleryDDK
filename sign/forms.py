from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group

class BasicLoginForm(LoginForm):
    user = forms.CharField(label = "Логин")
    pswd = forms.CharField(label = "Пароль")
    username = forms.CharField(max_length=30,)
    password = forms.CharField(max_length=30,)
    class Meta:
        model = User
        fields = ("username",
                  "password",)

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )