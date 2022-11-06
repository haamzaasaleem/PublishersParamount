from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

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
            current_user = AuthorProfileSerializer(Author.objects.get(user_id=user.id))
        elif user.role == 'editor':
            current_user = EditorProfileSerializer(Editor.objects.get(user_id=user.id))
        elif user.role == 'reviewer':
            current_user = ReviewerProfileSerializer(Reviewer.objects.get(user_id=user.id))
        elif user.role == 'eic':
            current_user = EicProfileSerializer(EditorInChief.objects.get(user_id=user.id))

        dict = serializer.data | current_user.data

        return Response(dict)

    def update(self, request, pk=None):
        user_id = request.user.id
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
        elif instance.role == 'reviewer':
            Reviewer.objects.get_or_create(user=instance)
        elif instance.role == 'eic_staff':
            EicStaff.objects.get_or_create(user=instance)
        elif instance.role == 'e_staff':
            EditorStaff.objects.get_or_create(user=instance)
        instance.save()


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(request.data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(request.data['new_password'])
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordview(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, pk=None):
        user = User.objects.get(id=request.user.id)
        if request.data['password'] != request.data['newPassword']:

            if user.check_password(request.data['password']):
                user.set_password(request.data['newPassword'])
                user.save()
                return Response(
                    {"msg": "Password Updated Successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"msg": "Password does not matched"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"msg": "You cannot use your current password again "},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgotPasswordView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, pk=None):
        user = User.objects.get(email=request.data['email'])

        if user:
            send_mail(
                f'Password Reset URL for USER: #{request.user.username}',

            )
