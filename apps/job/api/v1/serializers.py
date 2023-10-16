from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.account.api.v1.serializers import MyProfileSerializer
from apps.job.models import Category, Skill, Company, Job, Responsibility, ApplyJob


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'description', 'modified_date', 'created_date']


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['id', 'name', 'modified_date', 'created_date']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'image', 'location', 'modified_date', 'created_date']


class JobSerializer(serializers.ModelSerializer):
    from apps.account.api.v1.serializers import MyProfileSerializer
    author = MyProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    skills = SkillSerializer(read_only=True, many=True)
    job_type = serializers.CharField(source='get_job_type_display', read_only=True)
    experience = serializers.CharField(source='get_experience_display', read_only=True)
    salary = serializers.CharField(source='get_salary_display', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'author', 'title', 'icon', 'company', 'category', 'job_type', 'experience',
                  'salary', 'vacancy', 'description', 'skills', 'modified_date', 'created_date']


class JobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'author', 'title', 'icon', 'company', 'category', 'job_type', 'experience',
                  'salary', 'vacancy', 'description', 'skills', 'modified_date', 'created_date']
        extra_kwargs = {
            "author": {'read_only': True},
            "icon": {'required': True},
        }

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        if user.type != 0:
            raise ValidationError({"error": "User must be only HR"})
        user_companies_values = user.usercompanies.all().values_list('company_id')
        user_companies_lst = [_[0] for _ in user_companies_values]
        company = attrs.get('company', None)
        if company is not None:
            if company not in user_companies_lst:
                raise ValidationError({"error": "The company is not valid for user"})

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user_id = request.user.id
        skills = validated_data.pop('skills', [])
        instance = Job.objects.create(author_id=user_id, **validated_data)
        for skill in skills:
            instance.skills.add(skill)
        return instance

    def update(self, instance, validated_data):
        instance.skills.clear()
        skills = validated_data.pop('skills', [])
        instance = super().update(instance, validated_data)
        for skill in skills:
            instance.skills.add(skill)
        return instance


class ApplyJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    user = MyProfileSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ApplyJob
        fields = ['id', 'job', 'status', 'user']


class ApplyJobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyJob
        fields = ['id', 'job', 'status', 'user']
        extra_kwargs = {
            'user': {"read_only": True}
        }


    def validate(self, attrs):
        job = attrs.get('job')
        print(job)
        request = self.context['request']
        user_id = request.user.id
        apply_jobs = ApplyJob.objects.filter(user_id=user_id, job=job)
        for i in apply_jobs:
            if i.status in [0, 1]:
                raise ValidationError({"detail": "You already applied"})
        return attrs

    def create(self, validated_data):
        job = validated_data.get('job')
        print("create")
        print(job)
        request = self.context['request']
        user_id = request.user.id
        instance = ApplyJob.objects.create(job=job, user_id=user_id)
        return instance