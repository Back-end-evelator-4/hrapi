from django.conf import settings
from django.core.mail import send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import jwt
from apps.account.api.v1.serializers import RegisterSerializers, LoginSerializer, MyProfileSerializer, ChangePasswordSerializer, \
    SendResetLinkSerializer, SetPasswordSerializer
from apps.account.models import User
from apps.account.permissions import IsOwnerOrReadOnly


class RegisterAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/register/
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user).access_token

        abs_url = f"http://127.0.0.1:8000/account/api/v1/auth/verify-email/?token={token}"

        subject = "VERIFYING ACCOUNT FROM HR.UZ"
        message = f"Hi, {user.get_full_name}\n{abs_url}"
        sender = settings.EMAIL_HOST_USER
        receiver_list = [user.email]

        send_mail(subject, message, sender, receiver_list)

        return Response({"detail": "Verification link sent your mail"}, status=200)



class VerifyUserAPIView(APIView):
    # http://127.0.0.1:8000/account/api/v1/auth/verify-email/

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('token', openapi.IN_QUERY, description="Token",
                              type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(description='Success response'),
            400: openapi.Response(description='Bad request'),
        }
    )
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            return Response({"detail": f'{e}'}, status=400)
        else:
            user_id = decoded_token['user_id']
            user = User.objects.filter(id=user_id).first()
            if user:
                if user.is_active:
                    return Response({"detail": "You already verified"}, status=200)
                user.is_active = True
                user.save()
                return Response({"detail": "Account successfully verified"}, status=200)
            return Response({"detail": "User not found"}, status=404)


class LoginAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/login/
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = data.get('email')
        user = User.objects.filter(email__exact=email).first()
        refresh_token = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }
        return Response(tokens, status=200)


class MyProfileAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/my-profile/
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = MyProfileSerializer(user)
        return Response(serializer.data, status=200)


class MyProfileUpdateAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/my-profile/update/
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        obj = request.user
        serializer = self.get_serializer(data=request.data, instance=obj)
        serializer.is_valid(raise_exception=True)
        candidate = serializer.validated_data.pop('candidate')
        serializer.save()
        if candidate:
            skills = candidate.pop('skills', [])
            resume = candidate.pop('resume', None)
            category = candidate.pop('category', None)
            if resume:
                obj.candidate.resume = resume
            if category:
                obj.candidate.category = category
            if skills:
                obj.candidate.skills.clear()
                for skill in skills:
                    obj.candidate.skills.add(skill.id)
            obj.candidate.save()

        return Response(serializer.data)


class ChangePasswordAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/change-password/
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get('password')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(password)
        user.save()
        return Response({"detail": "Password changed"}, status=200)



"""
1. send unique link to email
2. set new password 
"""
class SendResetLinkAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/send-reset-link/
    queryset = User.objects.all()
    serializer_class = SendResetLinkSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email__exact=data.get('email'))
        token = RefreshToken.for_user(user).access_token
        abs_url = f"http://127.0.0.1:8000/account/api/v1/auth/set-password/?token={token}"

        subject = "SETTING NEW PASSWORD IN HR.UZ"
        message = f"Hi, {user.get_full_name}\n{abs_url}"
        sender = settings.EMAIL_HOST_USER
        receiver_list = [user.email]

        send_mail(subject, message, sender, receiver_list)

        return Response({"detail": "Verification link sent your mail"}, status=200)


class SetPasswordAPIView(GenericAPIView):
    # http://127.0.0.1:8000/account/api/v1/auth/set-password/
    queryset = User.objects.all()
    serializer_class = SetPasswordSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        token = request.GET.get('token')
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            return Response({"detail": f'{e}'}, status=400)
        else:
            user_id = decoded_token['user_id']
            user = User.objects.filter(id=user_id).first()
            if user:
                user.is_active = True
                user.set_password(password)
                user.save()
                return Response({"detail": "password changed"}, status=200)
            return Response({"detail": "User not found"}, status=404)

