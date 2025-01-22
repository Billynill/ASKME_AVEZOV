import copy

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.forms import LoginForm, UserForm, QuestionForm, RegistrationForm, UserUpdateForm, ProfileForm
from app.models import Tag, Post, Author, Answer, Profile
from django.contrib import auth
from django.contrib import messages


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

@csrf_exempt
def update_likes(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=post_id)

        if action == 'like':
            post.likes += 1
        elif action == 'dislike':
            post.dislikes += 1

        post.save()

        return JsonResponse({
            'likes': post.likes,
            'dislikes': post.dislikes
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.likes += 1
    answer.save()
    return redirect('one_question', question_id=answer.post.id)

def add_answer(request, question_id):
    post = get_object_or_404(Post, id=question_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        author, created = Author.objects.get_or_create(user=request.user)

        answer = Answer.objects.create(
            content=content,
            post=post,
            author=author
        )
        return redirect('one_question', question_id=post.id)
    return render(request, 'one_question.html', {'question': question})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            print("User form valid:", user_form.cleaned_data)
            print("Profile form valid:", profile_form.cleaned_data)
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('index')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })





