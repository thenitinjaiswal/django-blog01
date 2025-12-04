from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import CommentForm

def blog_detail(request, slug):
    """Display single post with comments and handle comment form."""
    post = get_object_or_404(Post, slug=slug, status='published')
    # post.increment_views()
    
    comments = post.comments.filter(active=True)
    
    # NEW: Get related posts
    related_posts = post.get_related_posts(count=3)
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,  # NEW: Add to context
    }
    
    return render(request, 'blog/detail.html', context)


def blog_category(request, category_name):
    """Display posts filtered by category."""
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(status='published', categories=category)
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    
    return render(request, 'blog/category.html', context)

def blog_index(request):
    """Display all published posts with search and pagination."""
    # OPTIMIZED: Use select_related for ForeignKey, prefetch_related for ManyToMany
    post_list = Post.objects.filter(status='published').select_related('author').prefetch_related('categories', 'tags')
    
    search_query = request.GET.get('search', '')
    if search_query:
        post_list = post_list.filter(
            Q(title__icontains=search_query) | 
            Q(body__icontains=search_query)
        )
    
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
    }
    
    return render(request, 'blog/index.html', context)

def blog_detail(request, slug):
    """Display single post with comments and handle comment form."""
    # OPTIMIZED: Prefetch related data
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('categories', 'tags'),
        slug=slug, 
        status='published'
    )
    post.increment_views()
    
    # OPTIMIZED: Only get active comments
    comments = post.comments.filter(active=True).order_by('created_on')
    
    related_posts = post.get_related_posts(count=3)
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/detail.html', context)

def blog_category(request, category_name):
    """Display posts filtered by category."""
    category = get_object_or_404(Category, name=category_name)
    
    # OPTIMIZED: Prefetch related data
    posts = Post.objects.filter(
        status='published', 
        categories=category
    ).select_related('author').prefetch_related('categories')
    
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    
    return render(request, 'blog/category.html', context)
