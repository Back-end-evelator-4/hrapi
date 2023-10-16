from django.urls import path, include

app_name = 'job'


urlpatterns = [
    path('v1/', include('apps.job.api.v1.urls'))
    
]
