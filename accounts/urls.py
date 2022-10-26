from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'password-reset', ResetPasswordview)

urlpatterns = [
    path('accounts/', include(router.urls)),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))
    
]
