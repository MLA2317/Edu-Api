from django.db import models
from django.db.models.signals import post_save
from app.main.models import Category, Tag
from django.conf import settings
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=221)
    image = models.ImageField(upload_to='blog/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Body(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_body')
    body = RichTextField()
    is_script = models.BooleanField(default=False)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments') # urldan oldik
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    top_level_comment_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"comment of {self.author} ({self.id})"

    @property # property - bu htmlda chaqirvolish uchun yoziladi yani nuqta bn chaqirladi
    def get_related_comments(self):
        qs = Comment.objects.filter(top_level_comment_id=self.id).exclude(id=self.id)
        if qs:
            return qs
        return None


def comment_post_save(instance, sender, created, *args, **kwargs):
    if created:
        top_level_comment = instance
        while top_level_comment.parent_comment:
            top_level_comment = top_level_comment.parent_comment
        instance.top_level_comment_id = top_level_comment.id
        instance.save()


post_save.connect(comment_post_save, sender=Comment)
