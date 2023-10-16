from rest_framework import generics, status, permissions, views
from rest_framework.response import Response

from apps.account.api.v1.serializers import MyProfileSerializer
from apps.blog.models import Blog, Comment
from .filters import BlogFilter
from .serializers import BlogSerializer, BlogPostSerializer, CommentSerializer, CommentPostSerializer
from ...permissions import IsOwnerOrReadOnly


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filterset_class = BlogFilter



class MyBlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = BlogFilter

    def get_queryset(self):
        qs = super().get_queryset().filter(author_id=self.request.user.id)
        return qs


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        obj_id = instance.data.get('id')
        obj = Blog.objects.get(id=obj_id)
        serializer = BlogSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = BlogSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogLikeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_blog_object(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog_obj = Blog.objects.get(id=blog_id)
        return blog_obj


    def get(self, request, *args, **kwargs):
        blog_obj = self.get_blog_object(*args, **kwargs)
        likes = blog_obj.likes.all()
        serializer = MyProfileSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        blog_obj = self.get_blog_object(*args, **kwargs)
        likes = blog_obj.likes.all()
        user = request.user
        if user in likes:
            blog_obj.likes.remove(user)
            return Response({"success": True, "detail": "Disliked"}, status=200)
        else:
            blog_obj.likes.add(user)
            return Response({"success": True, "detail": "Liked"}, status=200)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        blog_id = self.kwargs.get('blog_id')
        qs = qs.filter(blog_id=blog_id)
        return qs


class CommentPostAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super(CommentPostAPIView, self).get_serializer_context()
        ctx['blog_id'] = self.kwargs.get('blog_id')
        return ctx



