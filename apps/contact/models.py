from django.db import models
from apps.blog.models import BaseModel


class Contact(BaseModel):
    first_name = models.CharField(max_length=221)
    last_name = models.CharField(max_length=221)
    email = models.EmailField(max_length=221)
    subject = models.CharField(max_length=221)
    message = models.TextField()

