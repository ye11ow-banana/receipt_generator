from django.db.models import QuerySet

from .models import Printer, Check
from .tasks import check_generator


def get_printers_at_point(point_id: int) -> QuerySet[Printer]:
    """
    Get all QuerySet of Printer from db using point_id.
    """
    return Printer.objects.filter(point_id=point_id)


def is_printers_at_point_exists(point_id: int) -> bool:
    """
    Check if there are printers with this point_id in db.
    """
    printers = get_printers_at_point(point_id)
    return printers.exists()


def is_checks_with_order_id_exists(order_id: int) -> bool:
    """
    Check if there are checks with this order_id in db.
    """
    return Check.objects.filter(order__order_id=order_id).exists()


def get_list_of_check_instances(
        printers: QuerySet[Printer], order: dict) -> list[Check]:
    """
    Data for bulk_create of Check instances.
    """
    return [
        Check(
            printer=printer, type=printer.check_type, order=order
        ) for printer in printers
    ]


def bulk_create_checks(printers: QuerySet[Printer], order: dict) -> None:
    """
    Bulk create Checks for every printer.
    """
    check_instances = get_list_of_check_instances(printers, order)
    Check.objects.bulk_create(check_instances)


def create_checks_at_point(point_id: int, order_id: int, order: dict) -> None:
    """
    Create Checks with PDF file for every printer at a point.
    """
    printers = get_printers_at_point(point_id).only('check_type')
    bulk_create_checks(printers, order)
    for printer in printers:
        check_generator.delay(order_id, printer.check_type)
