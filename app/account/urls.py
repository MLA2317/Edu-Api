from django.urls import path, include

app_name = 'account'

urlpatterns = [
    path('v1/', include('app.account.v1.urls')),

    # api
    path('api/', include('app.account.api.urls')),
]
