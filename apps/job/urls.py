from django.urls import path, include

app_name = 'job'


urlpatterns = [
    path('api/', include('apps.job.api.urls')),
]
