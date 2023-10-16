from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    title = models.CharField(max_length=221)
    slug = models.SlugField(max_length=221, null=True, blank=True, editable=False, unique=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        url = reverse('blog:detail_page', args=[self.slug])
        return url



def post_pre_save(instance, sender, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(post_pre_save, sender=Post)
