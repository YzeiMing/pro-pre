from django.urls import path
from . import views

app_name = 'blogauth'

urlpatterns = [
    path('login/', views.login_blog, name='login'),
    #注意路由是不是要”/
    path('register/', views.register, name='register'),
    #注意路由是不是要”/
    path('captcha/', views.send_email_captcha, name='email-captcha'),
    path('logout/', views.blog_logout, name='logout'),
]