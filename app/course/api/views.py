from rest_framework import static, generics, permissions
from .serializer import CourseSerializer
from ..models import Course, SoldCourse, Lesson, LessonFiles
from rest_framework.pagination import PageNumberPagination


class CourseListCreate(generics.ListCreateAPIView):
    # https://127.0.0.1:8000/course/api/list-create/
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    page_size = 10
