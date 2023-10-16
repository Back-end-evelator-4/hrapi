from django.urls import path
from .views import BlogListAPIView, BlogCreateAPIView, BlogRUDAPIView, MyBlogListAPIView, BlogLikeAPIView, \
    CommentListAPIView, CommentPostAPIView


urlpatterns = [
    path('list/', BlogListAPIView.as_view()),
    path('list/my/', MyBlogListAPIView.as_view()),
    path('create/', BlogCreateAPIView.as_view()),
    path('detail/<int:pk>/', BlogRUDAPIView.as_view()),

    path('likes/<int:blog_id>/', BlogLikeAPIView.as_view()),

    path('comment/<int:blog_id>/', CommentListAPIView.as_view()),
    path('comment/<int:blog_id>/create/', CommentPostAPIView.as_view()),
]
