from rest_framework import serializers
from manuscripts.models import Manuscript


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = ['id','title','author','abstract','keywords','article_type','file']
