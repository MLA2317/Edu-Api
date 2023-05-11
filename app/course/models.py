from django.db import models
from django.conf import settings
from app.main.models import Category, Tag
from ckeditor.fields import RichTextField


class Timestamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def file_path_for_cover(instance, filename):
    return f"courses/{instance.id}/cover/{filename}"


class Course(Timestamp):
    DIFFICULTY = (
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Advanced'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 0})
    title = models.CharField(max_length=221)
    cover = models.ImageField(upload_to=file_path_for_cover, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    body = RichTextField()
    price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)  # 65.99
    discount_price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


def file_path(instance, filename):
    return f"courses/{instance.lesson.course.title}/{instance.lesson.title}/{filename}"


class Lesson(Timestamp):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    body = RichTextField()
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class LessonFiles(Timestamp):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  #/course_name/lesson_name/ files
    file = models.FileField(upload_to=file_path)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson.title


class SoldCourse(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 1})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} -> {self.course.title}"

