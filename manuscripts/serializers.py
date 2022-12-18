from rest_framework import serializers
from rest_framework.exceptions import *

from manuscripts.models import Manuscript, Figure, ManuRev, ManuEditor, CoAuthorModels


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = '__all__'



class FigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figure
        fields = '__all__'


class CoAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoAuthorModels
        fields = '__all__'


class ManuRevSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuRev
        fields = '__all__'


class ManuEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuEditor
        fields = '__all__'
