from django.urls import include, path
from rest_framework import routers
from .views import ManuscriptViewSet

router = routers.DefaultRouter()
router.register(r'manuscripts', ManuscriptViewSet)

urlpatterns = [
    path('manuscript/', include(router.urls)),
]
