from rest_framework import serializers
from manuscripts.models import Manuscript


class ManuscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = ['id','title','author','abstract','keywords','article_type','file']

    def validate_file_extension(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf','.doc','.docx']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')