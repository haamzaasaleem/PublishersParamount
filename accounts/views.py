from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenViewBase

from .models import Author, Editor, EditorInChief
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()
class LoginView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):

        user = request.user
        serializer = UserSerializer(user)
        if user.role == 'author':
            author = AuthorProfileSerializer(Author.objects.get(user_id=user.id))
        dict = serializer.data | author.data

        return Response(dict)

    def update(self, request,pk=None):
        user_id = request.user.id
        user_role = request.user.role

        user_data = {

            'email': request.data['email'],
            'gender': request.data['gender']
        }

        profile_data = {
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'bio': request.data['bio'],
            'phone': request.data['phone'],
            'address': request.data['address'],
            'user_image': request.data['user_image'],
        }
        profile = None
        if request.user.role == 'author':
            author = Author.objects.get(user_id=user_id)
            profile = AuthorProfileSerializer(author, data=profile_data, partial=True)
        if request.user.role == 'editor':
            editor = Editor.objects.get(user_id=user_id)
            profile = EditorProfileSerializer(editor, data=profile_data, partial=True)

        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid() and profile.is_valid():
            serializer.save()
            profile.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# class resetUserPasswordView(viewsets.ModelViewSet):
#     # queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # class partial_update(self, request):

#     #     user=User.objects.get(id=request.user.id)
#     #     serializer=UserSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.data.password=set_password(request.data.password)
#         serializer.save()
#         return Response({'msg':'Password Updated'})
#     return Response(serializer.errors,{"msg":"unable to update password"})


# class UserLoginViewset(APIView):

#     def post(self,request):

#         serializer=UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             if request.data['role'] is 'author':
#                 token=get_tokens_for_user()
#             return Response({"msg":"Student Created"},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
