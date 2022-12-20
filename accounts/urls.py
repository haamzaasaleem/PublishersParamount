from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'create-users', UserRegistration)
router.register(r'password-reset', ResetPasswordview)
# router.register(r'forgot-password', forgotPasswordView)

urlpatterns = [
    path('accounts/', include(router.urls)),
    path('accounts/journal-based-reviewers/<int:pk>/', JournalBasedReviewer, name='journal-based-reviewers'),
    path('accounts/journal-based-editors/<int:pk>/', JournalBasedEditors, name='journal-based-editors'),
    path('accounts/journal-based-eic/<int:pk>/', JournalBasedEic, name='journal-based-eic'),
    path('forget-password/<str:token>', forgotPasswordView),

]
