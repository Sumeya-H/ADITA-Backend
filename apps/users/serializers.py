import requests
from django.conf import settings
from .models import Staff, Student
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# ----------------------
# Staff Serializer
# ----------------------


class StaffCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Staff
        fields = ['email', 'phone_number', 'password',
                  'role', 'department', 'job_title']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Create user
        user = User.objects.create(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            is_staff=True
        )
        user.set_password(password)
        user.save()

        # Create Staff profile
        staff = Staff.objects.create(
            user=user,
            role=validated_data.get('role'),
            department=validated_data.get('department'),
            job_title=validated_data.get('job_title')
        )
        return staff


# ----------------------
# Student Serializer
# ----------------------
class StudentCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = ['username', 'last_name', 'first_name', 'email',
                  'phone_number', 'password', 'professional_background', 'country']

    def create_moodle_user(self, user, student, password):
        url = f"{settings.MOODLE_URL}/webservice/rest/server.php"

        payload = {
            "wstoken": settings.MOODLE_ADMIN_TOKEN,
            "wsfunction": "core_user_create_users",
            "moodlewsrestformat": "json",
            "users[0][username]": user.username,
            "users[0][password]": password,
            "users[0][email]": user.email,
            "users[0][firstname]": user.first_name,
            "users[0][lastname]": user.last_name,
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()

        return response.json()

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        # Create user
        user = User.objects.create(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            username=username,
            last_name=last_name,
            first_name=first_name,
            is_staff=False
        )
        user.set_password(password)
        user.save()

        # Create Student profile
        student = Student.objects.create(
            user=user,
            professional_background=validated_data.get(
                'professional_background'),
            country=validated_data.get('country')
        )

        response = self.create_moodle_user(user, student, password)

        student.moodle_user_id = response[0]['id']
        student.save(update_fields=["moodle_user_id"])

        return student


class StudentReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "email", "full_name", "country"]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

# ----------------------
# Login Serializer
# ----------------------


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
