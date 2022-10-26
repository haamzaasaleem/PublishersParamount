from rest_framework import serializers
from rest_framework.exceptions import *

from manuscripts.models import Manuscript


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = ['id', 'title', 'author', 'abstract', 'keywords', 'article_type', 'file', 'status', 'created']


    def validate_file_extension(self, value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')
