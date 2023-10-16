from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import ValidationError


from ...models import User, UserCompany, Candidate, UserExperience


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'bio', 'type']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValidationError('passwords did not match')
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6, max_length=68, write_only=True)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError('User not found')
        if not user.is_active:
            raise ValidationError('User is not active, you should verify first')
        return attrs


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ['resume', 'skills', 'category']


class MyProfileSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'bio', 'type', 'candidate',
                  'is_active', 'is_staff', 'is_superuser', 'last_login', 'modified_date', 'created_date']
        extra_kwargs = {
            'email': {'read_only': True},
            'type': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'last_login': {'read_only': True},
        }



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=68, write_only=True)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if user.check_password(old_password):
            if password != password2:
                raise ValidationError('new passwords did not match')
            return attrs
        raise ValidationError('old passwords did not match')


class SendResetLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email__exact=email).first()
        if user:
            return attrs
        raise ValidationError('email does not exist')


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValidationError('new passwords did not match')
        return attrs


class UserCompanyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = ['id', 'user', 'company']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate(self, attrs):
        user = self.context['request'].user
        if user.type != 0:
            raise ValidationError({"error_user_role": "User must be hr role"})
        return attrs

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        instance = UserCompany.objects.create(user_id=user_id, **validated_data)
        return instance


class UserCompanySerializer(serializers.ModelSerializer):
    from apps.job.api.v1.serializers import CompanySerializer
    user = MyProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = UserCompany
        fields = ['id', 'user', 'company']



class MiniUserCompanySerializer(serializers.ModelSerializer):
    from apps.job.api.v1.serializers import CompanySerializer
    company = CompanySerializer(read_only=True)

    class Meta:
        model = UserCompany
        fields = ['company']


class UserCompanyByUserSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField(read_only=True)

    def get_companies(self, obj):
        user_companies = obj.usercompanies.all()
        serializer = MiniUserCompanySerializer(user_companies, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'bio', 'type', 'companies',
                  'modified_date', 'created_date']


class UserExperiencePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExperience
        fields = ['id', 'user', 'company', 'category', 'start_date', 'end_date', 'is_now_work', 'modified_date', 'created_date']
        extra_kwargs = {
            'user': {'read_only': True}
        }


    def create(self, validated_data):
        user_id = self.context['request'].user.id
        instance = UserExperience.objects.create(user_id=user_id, **validated_data)
        return instance


class UserExperienceSerializer(serializers.ModelSerializer):
    from apps.job.api.v1.serializers import CompanySerializer, CategorySerializer
    user = MyProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = UserExperience
        fields = ['id', 'user', 'company', 'category', 'start_date', 'end_date', 'is_now_work', 'modified_date', 'created_date']






