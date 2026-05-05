from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

#用get_user_model()获取Django内置数据库的用户对象
User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'require': '必填',
        'max_length': '太长',
        'min_length': '太短',
    })
    email = forms.EmailField(error_messages={'require': '必填', 'invalid': '错误'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=3)

    #基本清洗后，通过数据验证来判读
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        #为什么还要返回email
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data['captcha']
        email = self.cleaned_data['email']
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('This captcha is invalid.')
        captcha_model.delete()
        # 为什么还要返回
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'require': '必填', 'invalid': '错误'})
    password = forms.CharField(max_length=20, min_length=3)
    remember = forms.IntegerField(required=False)
