from django.shortcuts import render
from django.views.decorators.http import require_GET
from . import models


def index(request):
    context = {'questions': models.QUESTIONS, 'is_auth': True}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item = models.QUESTIONS[question_id]
    context = {'answers': models.ANSWERS, 'question': question_item}
    return render(request, 'question.html', context=context)


def askq(request):
    return render(request, 'askq.html')


def register(request):
    return render(request, 'register.html')


def registration(request):
    return render(request, 'registration.html')


def settings(request):
    return render(request, 'settings.html')


def tags(request, tags_id: int):
    tags_item = models.TAGS[tags_id]
    context = {'tags': tags_item}
    return render(request, 'tags.html', context=context)