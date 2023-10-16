from rest_framework import serializers

from apps.blog.models import Blog, Comment
from apps.job.api.v1.serializers import CategorySerializer, SkillSerializer
from apps.account.api.v1.serializers import MyProfileSerializer

class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = SkillSerializer(read_only=True, many=True)
    author = MyProfileSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'image', 'description', 'category', 'tags', 'likes_count', 'modified_date', 'created_date']



class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'image', 'description', 'category', 'tags']
        extra_kwargs = {
            'author': {'read_only': True},
            'image': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        instance = super().create(validated_data)
        instance.author = user
        instance.save()
        return instance


class CommentMiniSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'parent', 'comment', 'modified_date', 'created_date']


class CommentSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        qs = Comment.objects.filter(top_level_comment_id=obj.id).exclude(id=obj.id)
        sz = CommentMiniSerializer(qs, many=True)
        return sz.data


    class Meta:
        model = Comment
        fields = ['id', 'author', 'comment', 'children', 'modified_date', 'created_date']


class CommentPostSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'comment', 'blog', 'parent', 'modified_date', 'created_date']
        extra_kwargs = {
            'blog': {'read_only': True}
        }


    def create(self, validated_data):
        request = self.context['request']
        user_id = request.user.id
        blog_id = self.context['blog_id']
        instance = Comment.objects.create(author_id=user_id, blog_id=blog_id, **validated_data)
        return instance



