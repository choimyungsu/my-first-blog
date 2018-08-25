# java의 controller 같은 역할
from django.shortcuts import render, get_object_or_404,redirect
# 페이징 처리 2018.08.19
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment, Book # 모델 임포트
from .forms import PostForm, CommentForm, BookForm # form 임포트 추가
from django.contrib.auth.decorators import login_required
# 검색을 위한 추가 2018.08.18 search.views.py
from itertools import chain 
from django.views.generic import ListView


def book_list(request): # 책리스트 가져오기
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # 페이징 처리 추가 2018.08.19
    paginator = Paginator(books, 8) # Show 9 contacts per page
    page = request.GET.get('page')
    try:
        #books = paginator.get_page(page)
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)       
  
    return render(request, 'blog/book_list.html', {'books': queryset})

@login_required
def my_book_list(request): # 내 책리스트 가져오기 2018.08.18
    books = Book.objects.filter(author= request.user).order_by('created_date')
    # 페이징 처리 추가 2018.08.19
    paginator = Paginator(books, 8) # Show 9 contacts per page
    page = request.GET.get('page')
    try:
        #books = paginator.get_page(page)
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages) 

    return render(request, 'blog/book_list.html', {'books': queryset})


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
    books = Book.objects.filter(published_date__isnull=True,author= request.user).order_by('created_date') # 저자책만 가져오기
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
    posts = book.posts.all() # filter 걸어야 함..로그인사용자, 또는 퍼블리쉬되지 않은 글 

    next_post = get_next_or_prev(posts, post, 'next')
    prev_post = get_next_or_prev(posts, post, 'prev')
    # aaa =book.posts.all #"cms 좀 나와라"
    # order = aaa.count()
    # #order =  # 북안에 Post가 몇번째 있는지 확인 
    # #book = get_object_or_404(Book, pk=post.book.id) # ??
    return render(request, 'blog/post_detail.html', {'post': post,'book':book,'next_post':next_post,'prev_post':prev_post}) #

# 앞뒤 객체 가져오기 https://gist.github.com/kvnn/2303613
''' Function '''
def get_next_or_prev(models, item, direction):
    '''
    Returns the next or previous item of
    a query-set for 'item'.

    'models' is a query-set containing all
    items of which 'item' is a part of.

    direction is 'next' or 'prev'
    
    맨처음/맨 마지막은 순환된다.(놔둬도 될까?)

    '''
    getit = False
    if direction == 'prev':
        models = models.reverse()
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        # This would happen when the last
        # item made getit True
        return models[0]
    return False 

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     book = Book.objects.get(id=post.book_id)
#     aaa = "adfasdfasdfasdfdasdf"
#     # order = book.index(post)# 북안에 Post가 몇번째 있는지 확인 

#     return render(request, 'blog/post_detail.html', {'post': post,'book':book,'aaa':aaa})

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
    return redirect('post_view', pk=pk)   
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

# def search(request):# 검색 페이지로 이동
#     return render(request, 'blog/view.html')  

# 검색 추가
class SearchView(ListView):
    template_name = 'blog/view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            book_results      = Book.objects.search(query)
            post_results      = Post.objects.search(query)
            comment_results   = Comment.objects.search(query)

            # combine querysets 
            queryset_chain = chain(
                    book_results,
                    post_results,
                    comment_results,
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Post.objects.none() # just an empty queryset as default


     