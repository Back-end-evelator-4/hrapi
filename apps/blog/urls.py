from django.urls import path, include

from .views import HomeView, DetailView, CreateView

app_name = 'blog'


urlpatterns = [
    path('api/', include('apps.blog.api.urls')),

    path('', HomeView.as_view(), name='homepage'),
    path('create/', CreateView.as_view(), name='create'),
    path('detail/<slug:slug>/', DetailView.as_view(), name='detail_page'),
]
