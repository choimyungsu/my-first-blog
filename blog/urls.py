from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from blog.views import SearchView # 통합 검색 추가 2018.08.19


urlpatterns = [
    url(r'^$', views.book_list, name='book_list'), # book list 가 보이도록 변경
    url(r'^mybook/$', views.my_book_list, name='my_book_list'), # My_book list 가 보이도록 추가
    url(r'^book/new/$', views.book_new, name='book_new'), # 새책 생성 
    url(r'^book/(?P<pk>\d+)/$', views.book_detail, name='book_detail'),# book 한건 보이도록
    url(r'^(?P<pk>\d+)/$', views.post_view, name='post_view'),# Post 한건은 오른쪽에 Post리스트는 왼쪽에 
    url(r'^book/(?P<pk>\d+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^book/(?P<pk>\d+)/publish/$', views.book_publish, name='book_publish'),
    url(r'^book/(?P<pk>\d+)/remove/$', views.book_remove, name='book_remove'),
    url(r'^book/(?P<pk>\d+)/post/$', views.add_post_to_book, name='add_post_to_book'), # book에 포스트 생성
    url(r'^book/drafts/$', views.book_draft_list, name='book_draft_list'), # 발행되지 않은 책 리스트

    url(r'^search/$', SearchView.as_view(), name='search' ), # 통합 검색 추가 2018.08.19

    # url(r'^$', views.post_list, name='post_list'), # 일단 주석처리 book list에서 book을 클릭시 Post list로 연결
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

    url(r'^summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)