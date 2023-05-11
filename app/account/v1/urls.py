from django.urls import path, reverse, reverse_lazy
from django.contrib.auth.views import LoginView, \
    PasswordChangeView, PasswordChangeDoneView, LogoutView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import RegisterView, logout_view, profile_info, profile_update, my_course
# from .views import login_view, register_view


urlpatterns = [
    # path('login/', login_view, name='login'),
    # path('register/', register_view, name='register')

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile_info/', profile_info, name='info'),
    path('profile_update/<int:pk>/', profile_update, name='update'),
    path('my_courses/', my_course, name='mycourses'),

    #changepassword
    path('password_change/',
         PasswordChangeView.as_view(template_name='account/change_password/change_password_form.html',
                                    success_url=reverse_lazy('account:change_done')),
         name='change_password'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='account/change_password/password_change_done.html'),
         name='change_done'),

    #passwordreset email jonatish
    path('password_reset/send/',
         PasswordResetView.as_view(
             template_name='account/reset_password/password_reset_form.html',
             email_template_name='account/reset_password/password_reset_email.html',  #bu emailga boradigan habar
             success_url=reverse_lazy('account:password_done')),
         name='password_reset',),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='account/reset_password/password_reset_done.html'),
         name='password_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(
             template_name='account/reset_password/password_reset_confirm.html',
             success_url=reverse_lazy("account:password_complete")),
         name='password_confirm', ),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='account/reset_password/password_reset_complete.html'),
         name='password_complete')
]
