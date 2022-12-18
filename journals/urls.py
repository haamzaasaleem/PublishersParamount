from django.urls import include, path
from rest_framework import routers
from journals.views import JournalViewSet,SubjectViewSet, SubjectWiseJournalAPI

router = routers.DefaultRouter()
router.register(r'journals', JournalViewSet)


SubjectRouter = routers.DefaultRouter()
SubjectRouter.register(r'all', SubjectViewSet)
urlpatterns = [
    path('journal/', include(router.urls)),
    path('subject/', include(SubjectRouter.urls)),
    path('subject-wise-journal/<int:pk>/', SubjectWiseJournalAPI, name='subject-wise-journal')
]
