from django import forms

from .models import Post, Comment, Book
from django_summernote import fields as summer_fields # 2018.08.16 cms add
from django_summernote.widgets import SummernoteWidget # 2018.08.17 


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'text', 'photo')
        #fields ='__all__' # 모든 필드를 보여줄때 

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
			'title' : forms.TextInput(attrs={'class': 'form-control','width':'100'}),
            #'text' : forms.Textarea(attrs={'class': 'form-control', 'rows':15}),
            'text': SummernoteWidget,
		}
    

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '댓글을 입력해주세요.'}),
        }        

