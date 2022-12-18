from journals.models import Journal
from journals.serialiazers import JournalSerializer, SubjectSerializer
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from .models import Subject
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class JournalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows journals to be viewed or edited.
    """
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def SubjectWiseJournalAPI(self, pk=None):
    try:
        journals = Journal.objects.filter(subject=pk)
        serializer = JournalSerializer(journals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"msg": "No Journal Found Under this Subject"})
