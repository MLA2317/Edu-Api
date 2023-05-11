from django.urls import path
from .views import CourseView, CourseDetail, lesson_detail

urlpatterns = [
    path('course/', CourseView.as_view(), name='course'),
    path('detail/<int:pk>/', CourseDetail.as_view(), name='detail'),
    path('detail/<int:course_id>/lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
]
