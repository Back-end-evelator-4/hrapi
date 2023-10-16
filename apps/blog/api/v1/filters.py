from django_filters import filterset
from apps.blog.models import Blog


class BlogFilter(filterset.FilterSet):
    first_name = filterset.CharFilter(lookup_expr='icontains', field_name='author__first_name')
    last_name = filterset.CharFilter(lookup_expr='icontains', field_name='author__last_name')

    class Meta:
        model = Blog
        fields = ['category', 'tags', 'first_name', 'last_name']
