from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save

from apps.blog.models import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError({"Email must be exist"})
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    TYPE = (
        (0, 'Hr'),
        (1, 'Candidate')
    )

    email = models.EmailField(max_length=221, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='users')
    first_name = models.CharField(max_length=221, null=True, blank=True)
    last_name = models.CharField(max_length=221, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    @property
    def get_full_name(self):
        name_list = []
        if self.last_name:
            name_list.append(self.last_name)
        if self.first_name:
            name_list.append(self.first_name)
        full_name = " ".join(name_list)
        return full_name

    def __str__(self):
        return self.email



class UserCompany(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'type': 0}, related_name='usercompanies')
    company = models.ForeignKey('job.Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


def resume_path(instance, filename):
    return 'users/{}/{}'.format(instance.user.email, filename)


class Candidate(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'type': 1})
    resume = models.FileField(upload_to=resume_path, null=True, blank=True)
    skills = models.ManyToManyField('job.Skill', blank=True)
    category = models.ForeignKey('job.Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email


class UserExperience(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('job.Company', on_delete=models.CASCADE)
    category = models.ForeignKey('job.Category', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_now_work = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


def user_post_save(sender, instance, created, *args, **kwargs):
    if created and instance.type == 1:
        Candidate.objects.create(user_id=instance.id)


post_save.connect(user_post_save, sender=User)
