from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'gender']
    
    
# class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=User
#         fields = ['username', 'password','role']   



# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
