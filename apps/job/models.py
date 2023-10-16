from django.db import models
from apps.blog.models import BaseModel
from apps.account.models import User


class Category(BaseModel):
    name = models.CharField(max_length=221)
    icon = models.ImageField(upload_to='categories/')
    description = models.TextField()

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=221)
    image = models.ImageField(upload_to='companies/')
    location = models.CharField(max_length=221)

    def __str__(self):
        return self.name


class Skill(BaseModel):
    name = models.CharField(max_length=221)

    def __str__(self):
        return self.name



class Job(BaseModel):

    JOB_TYPE = (
        (0, 'Full-time'),
        (1, 'Part-time'),
        (2, 'Remote'),
    )
    EXPERIENCE = (
        (0, 'No Experience'),
        (1, 'About year'),
        (2, '1-2 years'),
        (3, '3-5 years'),
        (4, 'more than 5 years'),
    )
    SALARY = (
        (0, '$0.00'),
        (1, '$300-$500'),
        (2, '$500-$1000'),
        (3, '$1000-$1500'),
        (4, '$1500+'),
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobs', limit_choices_to={
        'type': 0
    })
    title = models.CharField(max_length=221)
    icon = models.ImageField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    job_type = models.IntegerField(choices=JOB_TYPE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.IntegerField(choices=EXPERIENCE)
    salary = models.IntegerField(choices=SALARY)
    vacancy = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title


class Responsibility(BaseModel):
    name = models.CharField(max_length=221)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ApplyJob(BaseModel):
    STATUS = (
        (0, 'applied'),
        (1, 'confirmed'),
        (2, 'cancelled'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applyjobs')
    user = models.ForeignKey(User, limit_choices_to={'type': 1}, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)



class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='savedjobs')
    user = models.ForeignKey(User, limit_choices_to={'type': 1}, on_delete=models.CASCADE)

