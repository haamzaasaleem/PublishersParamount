
from journals.models import Journal
from journals.serialiazers import JournalSerializer
from rest_framework import permissions, viewsets
from rest_framework.response import Response


class JournalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows journals to be viewed or edited.
    """
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   