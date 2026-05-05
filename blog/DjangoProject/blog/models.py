from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name = "分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = "博客"
        ordering  = ('-pub_time',)

class BlogComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ('-pub_time',)