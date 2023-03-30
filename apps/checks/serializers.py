from rest_framework import serializers

from . import services
from checks.models import Check


class AddNewOrderSerializer(serializers.Serializer):
    point_id = serializers.IntegerField(min_value=0)
    order_id = serializers.IntegerField(min_value=1)
    products = serializers.JSONField()

    def validate_point_id(self, value: int) -> int:
        """
        Check if there are printers with this point_id in db.
        """
        if not services.is_printers_at_point_exists(value):
            raise serializers.ValidationError(
                'There is no printers at the point')
        return value

    def validate_order_id(self, value: int) -> int:
        """
        Check if there are no checks with this order_id in db.
        """
        if services.is_checks_with_order_id_exists(value):
            raise serializers.ValidationError({
                'msg': 'Check has been already added',
                'order_id': value,
            })
        return value


class RenderedChecksSerializer(serializers.ModelSerializer):
    """
    Check model serializer for checks that
    are ready to be printed at a point.
    """
    class Meta:
        model = Check
        fields = ('id', 'type', 'pdf_file')
