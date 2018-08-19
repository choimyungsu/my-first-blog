from django import forms

from .models import Post, Comment, Book
# summernoteWidget 추가 
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
        fields = ('title', 'url','text') # 이 순서대로 form이 구성된다.
        widgets = {
			'title' : forms.TextInput(attrs={'class': 'form-control','width':'100','placeholder': '목차 제목을 입력해주세요.'}),
            'url' : forms.TextInput(attrs={'class': 'form-control','width':'100','placeholder': '대표 이미지 URL을 입력해주세요.','alt':'class="img-responsive"'}),
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

