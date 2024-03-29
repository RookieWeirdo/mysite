from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
                        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
                        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    email = forms.CharField(label='邮箱',
                            widget=forms.EmailInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=5,
                               widget=forms.PasswordInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='再输一次密码',
                                     min_length=5,
                                     widget=forms.PasswordInput(
                                            attrs={'class': 'form-control', 'placeholder': '请再输一次密码'}))

    # 判断用户名是否存在，cleaned_data 就是读取表单返回的值，返回类型为字典dict型
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不正确')
        return password_again
