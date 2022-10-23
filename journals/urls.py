from django.urls import include, path
from rest_framework import routers
from journals.views import JournalViewSet

router = routers.DefaultRouter()
router.register(r'journals', JournalViewSet)

urlpatterns = [
    path('journal/', include(router.urls)),
]
