from django.urls import path, include

app_name = 'account'


urlpatterns = [
    path('api/', include('apps.account.api.urls')),
]
