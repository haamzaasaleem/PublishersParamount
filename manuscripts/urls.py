from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'manuscripts', ManuscriptViewSet)
router.register(r'save', SaveManuscriptView)
router.register(r'assigned_manuscript_rev', AssignedManuscript2Reviewer)
router.register(r'get_assigned_manuscript_editor', AssignedManuscript2Editor)
urlpatterns = [
    path('manuscript/', include(router.urls)),
    path('manuscript/assigned_manuscript_editor/', AssignManuscriptToEditor, name='assigned_manuscript_editor'),
    path('manuscript/saved-manuscripts/<int:pk>/', savedManuscript, name='saved-manuscripts'),
    path('manuscript/send-assigned-manuscripts/<int:pk>/', sendAssignedReviewers, name='send-assigned-manuscript'),
    path('manuscript/editor-decision/<int:pk>/', GiveReviewToAuthor, name='editor-decision'),
]
