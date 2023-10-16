from rest_framework import generics, status, permissions, pagination
from rest_framework.response import Response

from apps.account.models import UserCompany, User, Candidate, UserExperience
from apps.account.permissions import ExperienceIsOwnerOrReadOnly
from ..serializers import UserCompanyPostSerializer, UserCompanySerializer, UserCompanyByUserSerializer, \
    UserExperienceSerializer, UserExperiencePostSerializer


class UserCompanyCreateAPIView(generics.CreateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCompanyListAPIView(generics.ListAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanySerializer


class UserCompanyByUserListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(type=0)
    serializer_class = UserCompanyByUserSerializer
    filterset_fields = ['id']


class UserExperienceAPIView(generics.GenericAPIView):
    queryset = UserExperience.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated, ExperienceIsOwnerOrReadOnly]
    serializer_class = UserExperiencePostSerializer
    pagination_class = pagination.PageNumberPagination
    page_size = 10

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        qs = self.get_queryset().filter(user_id=user_id)
        serializer = UserExperienceSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)




class UserExperienceRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserExperience.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated, ExperienceIsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserExperienceSerializer
        return UserExperiencePostSerializer


