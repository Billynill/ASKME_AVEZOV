import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is the text for question {i}'
    }for i in range(30)
]

# Create your views here.
def index (request):
    page_obj, question = paginate(request, QUESTIONS, per_page=5)
    return render(
        request, 'index.html',
        context={'questions': question, 'page_obj': page_obj}
    )

def hot(request):
    hot_questions = QUESTIONS[::-1]
    page_obj, questions = paginate(request, hot_questions, per_page=5)
    return render(
        request, 'hot.html',
        context={'questions': questions, 'page_obj': page_obj}
    )
def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        context={'item': one_question})

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