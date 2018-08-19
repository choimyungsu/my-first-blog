#java 의 DAO 같은거
import re
from django import forms
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

# Book 모델 검색
class BookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(text__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

# Post 모델 검색
class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(text__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

# Comment 모델 검색
class CommentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(text__icontains=query))
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Book(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(blank=True, null=True)#만약 도중에 모델이 변경되면 기존값에 대해선 널추가가 됨..
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = BookManager() # 검색관련 추가 2018.08.19 

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Post(models.Model ): # cms 2018.08.17 models.Model -> summer_model.Attachment
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE) # book에 종속되므로 주석처리 
    book = models.ForeignKey('blog.Book', related_name='posts') # Post 링크 연결 추가
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(
            blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True) # 이미지 URL 연결 필드 2018.08.19 
    objects = PostManager() # 검색관련 추가 2018.08.19 

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    # 정렬순서를 title순으로..
    class Meta:
        ordering =['title']

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL) # 로그인 사용자만 
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)
    objects = CommentManager() # 검색관련 추가 2018.08.19 

    # 정렬순서를 최근순으로..
    class Meta:
        ordering =['-id']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

