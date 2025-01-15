import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from app.models import Tag, Post, Author

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is the text for question {i}'
    }for i in range(30)
]

# Create your views here.
def index (request):
    posts = Post.objects.select_related('author').all()
    page_obj, questions = paginate(request, posts, per_page=5)
    tags = Tag.objects.all()[:10]
    best_members = Author.objects.all()[:5]
    return render(
        request, 'index.html',
        context={'questions': questions,
                 'page_obj': page_obj,
                 'tags': tags,
                 'best_members': best_members,
                 }
    )

def hot(request):
    posts = Post.objects.select_related('author').order_by('-likes')
    page_obj, questions = paginate(request, posts, per_page=5)
    tags = Tag.objects.all()[:10]
    best_members = Author.objects.all()[:5]
    return render(
        request, 'hot.html',
        context={'questions': questions,
                 'page_obj': page_obj,
                 'tags': tags,
                 'best_members': best_members,
                 }
    )
def question(request, question_id):
    item = get_object_or_404(Post, id=question_id)
    tags = Tag.objects.all()[:10]
    best_members = Author.objects.all()[:5]
    return render(
        request, 'one_question.html',
        context={'item': item,
                 'popular_tags': tags,
                 'best_members': best_members
                 }
    )

def paginate(request, queryset, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj, page_obj.object_list