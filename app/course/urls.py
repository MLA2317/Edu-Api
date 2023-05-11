from django.urls import path, include

app_name = 'course'

urlpatterns = [
    path('v1/', include('app.course.v1.urls')),
    path('api/', include('app.course.api.urls')),

]
