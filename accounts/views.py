# from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions

from .models import Author, Editor, EditorInChief
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        # import pdb; pdb.set_trace()
        user=request.user

        serializer=UserSerializer(user)
        return Response(serializer.data)
    

    def perform_create(self, serializer):
        # instance.password=make_password(self.password)
        instance = serializer.save()
        if instance.role == 'author':
            Author.objects.get_or_create(user=instance)
        elif instance.role == 'editor':
            Editor.objects.get_or_create(user=instance)
        elif instance.role == 'eic':
            EditorInChief.objects.get_or_create(user=instance)
        instance.save()

class UserVS(viewsets.ViewSet):

    def list(self,request):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
    
    def retrieve(self,request):
        user=User.objects.get(user=request.user)
        serializer=UserSerializer(user)
        return Response(serializer.data)


# class UserLoginViewset(APIView):

#     def post(self,request):
        
#         serializer=UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             if request.data['role'] is 'author':
#                 token=get_tokens_for_user()
#             return Response({"msg":"Student Created"},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
