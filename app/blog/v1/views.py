from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, redirect
from app.blog.models import Post, Comment, Body, Category, Tag
from app.course.models import Course


# def blog(request):
#     ctx = {
#
#     }
#     return render(request, "blog/post_list.html", ctx)
#
#
# def detail(request, pk):
#     ctx = {
#
#     }
#     return render(request, 'blog/blog-single.html', ctx)


class Blog(generic.ListView):
    # template_name = 'blog/post_list.html' #app_name/<model_name>_list.html
    queryset = Post.objects.all()
    paginate_by = 2
    ordering = ('-id',)

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

    # def get(self, request, *args, **kwargs): #agar List db yozganda shuni ishlatamiz
    #     ctx = {
    #
    #     }
    #     return render(request, self.template_name, ctx)
    #
    # def post(self, request, *args, **kwargs):
    #     ctx = {
    #
    #     }
    #     return render(request, self.template_name, ctx)


class BlogDetail(generic.View):
    template_name = 'blog/blog-single.html'
    lookup_filed = 'pk'
    queryset = Post.objects.all()

    def get_object(self, pk):
        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            raise Http404()  # raise = bu butun prayektni toxtatadi except ichiga qaytarib beradi
        return post

    def get_context_data(self, pk, *args, **kwargs):
        ctx = {
            'object': self.get_object(pk)
        }
        return ctx

    def get(self, request, pk):  # get - bu malumotni karob kada ochiqligica yetkazib beradi
        ctx = self.get_context_data(pk)
        comments = Comment.objects.filter(post_id=pk, parent_comment__isnull=True)
        ctx['comments'] = comments
        return render(request, self.template_name, ctx)

    def post(self, request, pk, *args, **kwargs): # post - bu malumotni karobkada yopiq holatda va hech kmga korinmidigan qilib yetkazib beradi
        ctx = self.get_context_data(pk)

        if not request.user.is_authenticated:
            return redirect('account:login')

        comment_id = request.GET.get('comment_id', None)
        user_id = request.user.id
        body = request.POST.get('body')
        if body:
            obj = Comment.objects.create(author_id=user_id, post_id=pk, body=body, parent_comment_id=comment_id)
            return redirect(reverse('blog:blog_detail', kwargs={'pk': pk}) + f"#comments_{obj.id}")  # agar kwarglar bolsa reverse_lazy ishlatamiz
        return render(request, self.template_name, ctx)
