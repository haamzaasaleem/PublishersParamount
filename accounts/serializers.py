from dataclasses import field
from pyexpat import model
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data['user_id'] = token['user_id']
        user = User.objects.get(id=data['user_id'])
        data['user_role'] = user.role

        return data


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'gender','password']


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class EditorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = '__all__'


class ReviewerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = '__all__'


class EicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorInChief
        fields = '__all__'


class EicStaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EicStaff
        fields = '__all__'


class EditorStaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorStaff
        fields = '__all__'


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgetPassword
        fields = '__all__'
