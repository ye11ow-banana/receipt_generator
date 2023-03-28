from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services


class AddNewOrderView(APIView):
    """
    Create checks for every printer at a point for every new order.
    """

    def post(self, request: Request) -> Response:
        try:
            point_id = request.data['point_id']
            order_id = request.data['order_id']
        except KeyError:
            return Response(
                {'result': False, 'msg': 'Invalid request data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not services.is_printers_at_point_exists(point_id):
            return Response(
                {'result': False, 'msg': 'There is no printers at the point'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if services.is_checks_with_order_id_exists(order_id):
            return Response(
                {
                    'result': False,
                    'msg': 'Check has been already added',
                    'order_id': order_id,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        services.create_checks_at_point(point_id, order_id, request.data)

        return Response({'result': True}, status=status.HTTP_201_CREATED)


add_new_order = AddNewOrderView.as_view()
