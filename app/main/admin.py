from django.contrib import admin
from .models import Category, Tag, FAQ, Subscribe, Answer, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_date')
    search_fields = ('name', 'email')
    date_hierarchy = 'created_date'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('id', 'question',)
    search_fields = ('email',)

