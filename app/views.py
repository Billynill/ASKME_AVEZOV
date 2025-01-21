import copy

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from app.forms import LoginForm, UserForm, QuestionForm, RegistrationForm
from app.models import Tag, Post, Author
from django.contrib import auth

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is the text for question {i}'
    }for i in range(30)
]

# Create your views here.
def index (request):
    posts = Post.objects.select_related('author').all().order_by('author_id')
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

def login (request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return  redirect('index')
            form.add_error('password', 'Invalid username or password.')
    return render(request, 'Login.html', context={'form': form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

def registration (request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registrationpage.html', context={'form': form})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Post saved successfully!')
        else:
            print(f"Ошибка здесь{form.errors}")
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', context={'form': form})

@login_required
def like_dislike(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exists'}, status=404)

        if action == 'like':
            post = Post.objects.add_like(post)
            return JsonResponse({'new_likes': post.likes})
        elif action == 'dislike':
            post = Post.objects.remove_like(post)
            return JsonResponse({'new_dislikes': post.likes})

        return JsonResponse({'error': 'Invalid action'}, status=400)
    return JsonResponse({'error': 'Invalid action'}, status=400)

