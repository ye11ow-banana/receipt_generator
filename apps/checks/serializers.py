from rest_framework.serializers import ModelSerializer

from checks.models import Check


class RenderedChecksSerializer(ModelSerializer):
    """
    Check model serializer for checks that
    are ready to be printed at a point.
    """
    class Meta:
        model = Check
        fields = ('id', 'type', 'pdf_file')
