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
    path('forget-password/<str:token>', forgotPasswordView),
    # path('accounts/', include(router.urls)),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('password_reset/', include(router.urls),
    # path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
