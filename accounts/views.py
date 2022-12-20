from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .models import *

from rest_framework.decorators import api_view, permission_classes
import uuid
from .mailer import *

User = get_user_model()


# class UserRegistration(viewsets.ModelViewSet):

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
        if request.user.role == 'reviewer':
            editor = Reviewer.objects.get(user_id=user_id)
            profile = ReviewerProfileSerializer(editor, data=profile_data, partial=True)

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


class ResetPasswordview(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, pk=None):

        user = User.objects.get(id=request.user.id)
        if request.data['newPassword'] == request.data['confirmPassword']:
            if request.data['currPassword'] != request.data['newPassword']:

                if user.check_password(request.data['currPassword']):
                    user.set_password(request.data['newPassword'])
                    user.save()
                    resetAuthPasswordMailer(user)
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
        else:
            return Response(
                {"msg": "Password and Confirm Password Does not match"},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))
def forgotPasswordView(request, token=None):
    if request.method == 'POST':
        if request.data['data'].find('@'):
            try:
                user = User.objects.get(email=request.data['data'])
            except:
                user = None
        else:
            try:
                user = User.objects.get(username=request.data['data'])
            except:
                user = None

        if user is not None:
            uuidToken = str(uuid.uuid4().hex)
            data = {
                "user": user.id,
                "token": uuidToken
            }
            serializer = ForgotPasswordSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                isSent = resetPasswordMailer(user, request.data['data'])
                if isSent:
                    return Response({"msg": "Email Sent!!",
                                     "data": serializer.data},
                                    status=status.HTTP_200_OK
                                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "User not Found"})

    if request.method == 'GET':
        try:
            dbToken = ForgetPassword.objects.get(token=token)
        except:
            return Response({"msg": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):

        user_data = {
            'email': request.data['email'],
            'gender': request.data['gender'],
            # 'password': request.data['password'],
            'password': make_password(request.data['password']),
            'username': request.data['username'],
            'role': request.data['role'],
        }

        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=user_data['username'])
            profile_data = {
                'user': str(user.id),
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'bio': request.data['bio'],
                'phone': request.data['phone'],
                'address': request.data['address'],

                # 'user_image': request.data['user_image'],
            }
            profileSerializer = None
            if user.role == 'author':
                profileSerializer = AuthorProfileSerializer(data=profile_data)
            elif user.role == 'editor':
                profileSerializer = EditorProfileSerializer(data=profile_data)
            elif user.role == 'eic':
                profileSerializer = EicProfileSerializer(data=profile_data)
            elif user.role == 'reviewer':
                profileSerializer = ReviewerProfileSerializer(data=profile_data)

            elif user.role == 'eic_staff':
                profileSerializer = EicStaffProfileSerializer(data=profile_data)
            elif user.role == 'e_staff':
                profileSerializer = EditorStaffProfileSerializer(data=profile_data)

            if profileSerializer.is_valid():
                profileSerializer.save()
                if user_data['role'] == 'reviewer':
                    rev = Reviewer.objects.get(user=profile_data['user'])
                    rev_data = {
                        'journal': request.data['journal'],
                        'education': request.data['education'],
                        'cv': request.data['cv']
                    }
                    revSerializer = ReviewerProfileSerializer(rev, data=rev_data, partial=True)
                    if revSerializer.is_valid():
                        revSerializer.save()
                        return Response(
                            {"msg": "User Created!"},
                            status=status.HTTP_201_CREATED)
                # userRegistrationMailer(user_data, profile_data)
                return Response(
                    {"msg": "User Created!"},
                    status=status.HTTP_201_CREATED)
            return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def JournalBasedReviewer(request, pk=None):
    reviewer = Reviewer.objects.filter(journal=pk)
    serializer = ReviewerProfileSerializer(reviewer, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def JournalBasedEditors(request, pk=None):
    editor = Editor.objects.filter(journal=pk)
    serializer = EditorProfileSerializer(editor, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def JournalBasedEic(request, pk=None):
    eic = EditorInChief.objects.filter(journal=pk)
    serializer = EicProfileSerializer(eic, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
