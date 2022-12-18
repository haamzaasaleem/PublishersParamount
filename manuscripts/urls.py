from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'manuscripts', ManuscriptViewSet)
router.register(r'save', SaveManuscriptView)
router.register(r'assigned_manuscript_rev', AssignedManuscript2Reviewer)
router.register(r'get-assigned_manuscript_editor', AssignedManuscript2Editor)
urlpatterns = [
    path('manuscript/', include(router.urls)),
    path('manuscript/assigned_manuscript_editor/', AssignManuscriptToEditor,name='assigned_manuscript_editor'),
    path('manuscript/saved-manuscripts/<int:pk>/', savedManuscript, name='saved-manuscripts'),
]
