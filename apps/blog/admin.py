from django.contrib import admin
from .old_models import Post
from .models import Blog, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    readonly_fields = ['slug']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'category', 'title', 'created_date']
    readonly_fields = ['likes', 'modified_date', 'created_date']
    date_hierarchy = 'created_date'
    search_fields = ['title', 'author__first_name', 'author__last_name', 'author__email']
    list_filter = ['category', 'tags']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'blog', 'created_date']
    readonly_fields = ['modified_date', 'created_date']
    date_hierarchy = 'created_date'
