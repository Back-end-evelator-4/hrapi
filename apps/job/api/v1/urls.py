from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, SkillViewSet, CompanyViewSet, JobListAPIView, JobPostAPIView, JobRUDAPIView, \
    MyJobsHrAPIView, SavedJobCandidateAPIView, ApplyJobAPIView, MyJobRequestAPIView, ResponseJobAPIView

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('skill', SkillViewSet)
router.register('company', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('jobs/list/', JobListAPIView.as_view()),
    path('jobs/create/', JobPostAPIView.as_view()),
    path('jobs/detail/<int:pk>/', JobRUDAPIView.as_view()),
    path('jobs/list/my/', MyJobsHrAPIView.as_view()),
    path('jobs/saved/', SavedJobCandidateAPIView.as_view()),
    path('jobs/apply/', ApplyJobAPIView.as_view()),
    path('jobs/request/', MyJobRequestAPIView.as_view()),
    path('jobs/send/response/', ResponseJobAPIView.as_view()),
]


"""
    apply job (c) +
    saved job (c) +
    
    my jobs (h) +
    my apply job (c) +
    
    my job request (h) +
    do response (h) +
    
    my apply job result (c) +
    
"""