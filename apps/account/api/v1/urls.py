from django.urls import path, include
from .views import RegisterAPIView, VerifyUserAPIView, LoginAPIView, MyProfileAPIView, ChangePasswordAPIView, \
    SendResetLinkAPIView, SetPasswordAPIView, UserCompanyCreateAPIView, UserCompanyListAPIView, \
    UserCompanyByUserListAPIView, MyProfileUpdateAPIView, UserExperienceAPIView, UserExperienceRUDAPIView



urlpatterns = [
    # auth
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/verify-email/', VerifyUserAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/my-profile/', MyProfileAPIView.as_view()),
    path('auth/my-profile/update/', MyProfileUpdateAPIView.as_view()),
    path('auth/change-password/', ChangePasswordAPIView.as_view()),

    path('auth/send-reset-link/', SendResetLinkAPIView.as_view()),
    path('auth/set-password/', SetPasswordAPIView.as_view()),

    # profile
    path('profile/user-company/create/', UserCompanyCreateAPIView.as_view()),
    path('profile/user-company/', UserCompanyListAPIView.as_view()),
    path('profile/user-company/by-user/', UserCompanyByUserListAPIView.as_view()),
    path('profile/experience/',  UserExperienceAPIView.as_view()),
    path('profile/experience/detail/<int:pk>/',  UserExperienceRUDAPIView.as_view()),

]
