from django.urls import path
from . import views


urlpatterns = [
    path('list-create/', views.CourseListCreate.as_view()),

]