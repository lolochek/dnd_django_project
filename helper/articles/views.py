from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, ArticleSearchForm
from .models import Article
from handbook.models import Comment

from handbook.forms import CommentForm


# Create your views here.


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article_content_type = ContentType.objects.get_for_model(Article)

    comments = Comment.objects.filter(
        content_type=article_content_type,
        object_id=article.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = article_content_type
            comment.object_id = article.id
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            return redirect('article_detail', pk=article.pk)

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

def article_list(request):
    form = ArticleSearchForm(request.GET)
    articles = Article.objects.order_by('-created_at')


    if form.is_valid():
        search = form.cleaned_data.get('search')
        author = form.cleaned_data.get('author')

        if search:
            articles = articles.filter(Q(title__icontains=search) | Q(content__icontains=search))

        if author:
            articles = articles.filter(author=author)

    return render(request, 'articles/article_list.html', {'form': form, 'articles': articles})