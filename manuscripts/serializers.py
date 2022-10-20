from rest_framework import serializers
from manuscripts.models import Manuscript


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = '__all__'
