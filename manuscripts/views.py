from rest_framework import permissions, viewsets
from manuscripts.models import Manuscript
from manuscripts.serializers import ManuscriptSerializer


class ManuscriptViewSet(viewsets.ModelViewSet):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
