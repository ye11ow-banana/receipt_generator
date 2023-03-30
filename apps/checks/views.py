from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from . import services
from .models import Check
from .serializers import RenderedChecksSerializer, AddNewOrderSerializer


class AddNewOrderView(APIView):
    """
    Create checks for every printer at a point for every new order.
    """

    def post(self, request: Request) -> Response:
        serializer = AddNewOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(dict(result=False, errors=serializer.errors))
        order_id = serializer.validated_data['order_id']
        point_id = serializer.validated_data['point_id']

        services.create_checks_at_point(point_id, order_id, request.data)

        return Response({'result': True}, status=status.HTTP_201_CREATED)


class GetRenderedChecksAtPointView(ListAPIView):
    """
    Get all Checks that are ready to be
    printed at a point with status changing.
    """
    serializer_class = RenderedChecksSerializer

    def get_queryset(self) -> QuerySet[Check]:
        return services.get_rendered_checks_at_point(self.kwargs['point'])

    def get(self, request: Request, *args, **kwargs) -> Response:
        response = self.list(request, *args, **kwargs)
        checks = self.get_queryset()
        services.set_printed_checks_status(checks)
        return response


add_new_order = AddNewOrderView.as_view()
get_rendered_checks_at_point = GetRenderedChecksAtPointView.as_view()
