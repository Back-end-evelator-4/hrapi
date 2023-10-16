from django.urls import path, include

app_name = 'blog'


urlpatterns = [
    path('v1/', include('apps.blog.api.v1.urls'))
    
]
