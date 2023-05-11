from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from ..models import Course, Lesson, LessonFiles
from app.main.models import Category, Tag


class CourseView(ListView):
    queryset = Course.objects.all()
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['categories'] = Category.objects.all()
        ctx['tags'] = Tag.objects.all()
        ctx['recent_courses'] = Course.objects.order_by("-id")[:3]
        return ctx


    def get_queryset(self):  # moshlashuvchan filterlar
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        q_conditions = Q()
        if q:
            q_conditions = Q(title__icontains=q)
        cat_conditions = Q()
        if cat:
            cat_conditions = Q(category__title__exact=cat)
        tag_conditions = Q()
        if tag:
            tag_conditions = Q(tags__title__exact=tag)
        qs = qs.filter(q_conditions, cat_conditions, tag_conditions)
        return qs


class CourseDetail(DetailView):
    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_courses'] = Course.objects.order_by('-id')[:3]
        ctx['categories'] = Category.objects.all()
        ctx['tags'] = Tag.objects.all()
        ctx['random_5_course'] = Course.objects.order_by('?')[:5]
        return ctx


def post_view(request, pk):
    obj = Lesson.objects.get(id=pk)
    obj.views += 1
    obj.save()
    return redirect(reverse('project:lesson_detail', kwargs={'pk': pk}))


def lesson_detail(request, course_id,  pk):
    lesson = Lesson.objects.get(id=pk)
    main_lessons = LessonFiles.objects.filter(lesson_id=pk, is_main=True).first() #true - boganda har doim bitta boladi
    random_5_course = Course.objects.order_by('?')[:5]
    ctx = {
        'lesson': lesson,
        'main_lesson': main_lessons,
        'random_5_courses': random_5_course,
    }
    return render(request, 'course/course_lesson.html', ctx)
