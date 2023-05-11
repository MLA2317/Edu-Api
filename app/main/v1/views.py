from django.shortcuts import render, redirect
from .forms import ContactForm, SubscribeForm
from ..models import Category, Tag, Contact, Subscribe, Answer, FAQ
from app.blog.models import Comment, Body, Post
from app.course.models import Course, Lesson, LessonFiles
from django.conf import settings

Profile = settings.AUTH_USER_MODEL


def index(request):
    categories = Category.objects.all()
    random_5_course = Course.objects.order_by('?')[:5]  # ? - bu istalgan tartibda taxlanadi
    teacher = Profile.objects.filter(role=0).order_by('?')[:3]
    last_post = Post.objects.last()
    resent_post = Post.objects.exclude(id=last_post.id).order_by('-id')[:4]
    ctx = {
        'categories': categories,
        'randomly_5_courses': random_5_course,
        'teachers': teacher,
        'last_post': last_post,
        'resent_posts': resent_post,
    }
    return render(request, 'main/index.html', ctx)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('.')
    forms = SubscribeForm(request.POST or None)
    if forms.is_valid():
        forms.save()
    ctx = {
        "form": form,
        'forms': forms
    }
    return render(request, 'main/contact.html', ctx)


def about(request):
    faq = FAQ.objects.all()
    answer = Answer.objects.all()
    ctx = {
        'faqs': faq,

    }
    return render(request, 'main/about.html', ctx)
