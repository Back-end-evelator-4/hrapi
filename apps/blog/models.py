from django.db import models
from django.db.models.signals import pre_save


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def blog_image_path(instance, filename):
    return "blog/{}/{}".format(instance.author_id, filename)


class Blog(BaseModel):
    author = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    title = models.CharField(max_length=221)
    image = models.ImageField(upload_to=blog_image_path)     # media/blog/{author_id}/test.jpg
    description = models.TextField()
    category = models.ForeignKey('job.Category', on_delete=models.SET_NULL, null=True, related_name='category_blogs')
    tags = models.ManyToManyField('job.Skill')
    likes = models.ManyToManyField('account.User')


    def __str__(self):
        return self.title


    @property
    def likes_count(self):
        return self.likes.count()


class Comment(BaseModel):
    author = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    top_level_comment_id = models.IntegerField(null=True, blank=True)




def comment_pre_save(instance, sender,  *args, **kwargs):
    current = instance
    while current.parent:
        current = current.parent
    instance.top_level_comment_id = current.id


pre_save.connect(comment_pre_save, sender=Comment)
