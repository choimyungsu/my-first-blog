from django import forms

from .models import Post, Comment, Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'text', 'photo')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)        