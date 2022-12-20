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
    path('manuscript/published-manuscript/', listApprovedArticles, name='published-manuscript'),
    path('manuscript/approved-journal-manuscript/<int:pk>/', listApprovedJournalArticles, name='approved-journal-manuscript'),
    path('manuscript/add-reviewer/', addReviewer, name='add-reviewer'),
    path('manuscript/check-assign-manuEditor/<int:pk>/', checkAssignedManuToEditor, name='check-assign-manuEditor'),
    path('manuscript/plag-webhook/', plagCheckWebhook, name='check-assign-manuEditor'),
    path('manuscript/send-email-for-reviewer-approval/', sendEmailforReviewerApproval, name='send-email-for-reviewer-approval'),
    path('manuscript/list-manuscript-AllowAny/<int:pk>/', listManuscriptANY, name='list-manuscript-AllowAny'),
]
