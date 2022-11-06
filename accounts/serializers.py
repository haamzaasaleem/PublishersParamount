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
        fields = ['id', 'username', 'email', 'role', 'gender']


class AuthorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'bio', 'phone', 'address']


class EditorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: Editor
        fields = '__all__'


class ReviewerProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: Reviewer
        fields = '__all__'


class EicProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: EditorInChief
        fields = '__all__'


# class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=User
#         fields = ['username', 'password','role']   


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class ChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']
