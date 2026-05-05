import random
from django.shortcuts import render,redirect, reverse
from django.http.response import JsonResponse
import string
from django.core.mail import send_mail


from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
#只能用auth里面的user对象才能使用这个login
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

# Create your views here.
@require_http_methods(["GET", 'POST'])
def login_blog(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            user = User.objects.filter(email=email).first()
            #检查加密密码与明文密码
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print("密码错误")
                #form.add_error('email','错误')
                #return render(request,'login.html',{'form':form})
                return redirect(reverse('blogauth:login'))

def blog_logout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            #password加密后存储，和User()不一样
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse("blogauth:login"))
        else:
            print(form.errors)
            return redirect(reverse("blogauth:register"))
            #return render(request,'register.html',{'form':form})

def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400, "message":"请填写邮箱"})
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("注册验证码", message=f"您的注册验证码是：{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code":200, "message":"邮箱验证码发送成功"})

