"""
URL configuration for ASKME_AVEZOV project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from ASKME_AVEZOV import settings
from app import views
urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registrationpage'),
    path('add-question/',  views.add_question, name='add_question'),
    path('update_likes/', views.update_likes, name='update_likes'),
    path('question/add/', views.add_question, name='add_question'),
    path('question/<int:question_id>/', views.question, name='one_question'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    path('question/<int:question_id>/add-answer/', views.add_answer, name='add_answer'),
    path('profile/edit', views.edit_profile, name='edit_profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def custom_404(request, exception):
    return  render(request, '404.html', status=404)
handler404 = custom_404
