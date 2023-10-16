from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.job.models import Category, Skill, Company, Job, SavedJob, ApplyJob
from config import settings
from .serializers import CategorySerializer, SkillSerializer, CompanySerializer, JobSerializer, JobPostSerializer, \
    ApplyJobSerializer, ApplyJobPostSerializer
from ...permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly, IsHR, IsCandidate


class CategoryViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.filter(is_deleted=False)
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class CompanyViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    queryset = Company.objects.filter(is_deleted=False)
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.filter(is_deleted=False)
    serializer_class = JobSerializer


class JobPostAPIView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Job.objects.filter(is_deleted=False)
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        obj_super = super().create(request, *args, **kwargs)
        obj = Job.objects.get(id=obj_super.data.get('id'))
        sz = JobSerializer(obj)
        return Response(sz.data, status=201)


class JobRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.filter(is_deleted=False)
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        obj_super = super().put(request, *args, **kwargs)
        obj = Job.objects.get(id=obj_super.data.get('id'))
        sz = JobSerializer(obj)
        return Response(sz.data, status=201)

    def patch(self, request, *args, **kwargs):
        obj_super = super().patch(request, *args, **kwargs)
        obj = Job.objects.get(id=obj_super.data.get('id'))
        sz = JobSerializer(obj)
        return Response(sz.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        sz = JobSerializer(obj)
        return Response(sz.data, status=201)


class MyJobsHrAPIView(generics.ListAPIView):
    queryset = Job.objects.filter(is_deleted=False)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsHR]

    def get_queryset(self):
        qs = super(MyJobsHrAPIView, self).get_queryset()
        return qs.filter(author_id=self.request.user.id)


class SavedJobCandidateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        user_id = self.request.user.id
        saved_jobs = Job.objects\
            .select_related('company', 'category', 'author')\
            .prefetch_related('savedjobs', 'skills')\
            .filter(savedjobs__user_id=user_id).distinct()
        return saved_jobs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = JobSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type="object",
            properties={
                "job_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["job_id"],
            example={
                "job_id": None,
            }
        ),
        responses={
            200: openapi.Response(description='Success response'),
            400: openapi.Response(description='Bad request'),
        }
    )
    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        if job in self.get_queryset():
            SavedJob.objects.get(job_id=job_id, user_id=request.user.id).delete()
            return Response({"detail": "Job removed from saved list"})
        SavedJob.objects.create(job=job, user_id=request.user.id)
        return Response({"detail": "Job added to saved list"})



class ApplyJobAPIView(generics.ListCreateAPIView):
    queryset = ApplyJob.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ApplyJobSerializer
        return ApplyJobPostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)



class MyJobRequestAPIView(generics.ListAPIView):
    queryset = ApplyJob.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated, IsHR]
    serializer_class = ApplyJobSerializer
    filterset_fields = ['status']

    def get_queryset(self):
        user_id = self.request.user.id
        qs = super().get_queryset()
        return qs.filter(job__author_id=user_id)


class ResponseJobAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsHR]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type="object",
            properties={
                "apply_job_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "status": openapi.Schema(type=openapi.TYPE_INTEGER),
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["apply_job_id", "status", "message"],
            example={
                "apply_job_id": None,
                "status": None,
                "message": "",
            }
        ),
        responses={
            200: openapi.Response(description='Success response'),
            400: openapi.Response(description='Bad request'),
        }
    )
    def post(self, request, *args, **kwargs):
        apply_job_id = request.data.get('apply_job_id')
        status = request.data.get('status')
        message = request.data.get('message')
        apply_job = get_object_or_404(ApplyJob, id=apply_job_id)
        apply_job.status = status
        apply_job.save()
        subject = apply_job.job.title
        message = f"Hi {apply_job.user.get_full_name}.\n{message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [apply_job.user.email]
        send_mail(subject, message, from_email, recipient_list)
        return Response({"detail": "Your message sent email of candidate"})






