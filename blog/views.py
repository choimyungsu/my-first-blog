# java의 controller 같은 역할
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post, Comment, Book # 모델 임포트
from .forms import PostForm, CommentForm, BookForm # form 임포트 추가
from django.contrib.auth.decorators import login_required


def book_list(request): # 책리스트 가져오기
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/book_list.html', {'books': books})
@login_required
def book_new(request):
    # request.POST, request.FILES
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            #post.published_date = timezone.now() # 북 발행은 별도로 수행
            book.save()
            #return redirect('book_detail', pk=book.pk) # book 상세
            return redirect('book_list')  # book list
    else:
        form = BookForm()
    return render(request, 'blog/book_edit.html', {'form': form})    
def book_detail(request, pk): # 책 상세내역 가져오기
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'blog/book_detail.html', {'book': book})    
@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            #post.published_date = timezone.now() # 포스트 발행은 별도로 수행
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'blog/book_edit.html', {'form': form}) 
@login_required
def book_draft_list(request):# 
    books = Book.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/book_draft_list.html', {'books': books}) # 'books'라는 변수이름으로 books를 넘김.
@login_required
def book_publish(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.publish()
    return redirect('book_detail', pk=pk)   
@login_required
def book_remove(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')  
@login_required
def add_post_to_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.book = book # 포린키 연결..
            post.save()
            return redirect('book_detail', pk=book.pk)# 
    else:
        form = PostForm()
    return render(request, 'blog/add_post_to_book.html', {'form': form,'book':book})


def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    book = Book.objects.get(id=post.book_id)
    #book = get_object_or_404(Book, pk=post.book.id) # ??
    return render(request, 'blog/post_detail.html', {'post': post,'book':book}) #




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    book = Book.objects.get(id=post.book_id)
    return render(request, 'blog/post_detail.html', {'post': post,'book':book})

@login_required
def post_new(request):
    # request.POST, request.FILES
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})   
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_view', pk=post.pk)
    else:
        form = PostForm(instance=post)
        book = Book.objects.get(id=post.book_id)
    return render(request, 'blog/post_edit.html', {'form': form,'book':book}) 
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)   
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    book = Book.objects.get(id=post.book_id)
    book_pk = book.pk
    post.delete()
    return redirect('book_detail', pk=book_pk)   
    #return redirect('post_list')   
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    book = Book.objects.get(id=post.book_id)
    if request.method == "POST":# *** 어느때
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_view', pk=post.pk)
    else:#.. 어느때?
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form,'book': book,'post':post})  


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_view', pk=comment.post.pk)
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_view', pk=comment.post.pk)    