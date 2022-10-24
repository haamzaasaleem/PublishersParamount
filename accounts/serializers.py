from dataclasses import field
from pyexpat import model
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import *

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'gender' ]


class AuthorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'bio', 'phone', 'address']


class EditorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model: Editor
        fields = ('__all__')

# class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=User
#         fields = ['username', 'password','role']   


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
