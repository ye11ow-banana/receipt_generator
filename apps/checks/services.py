from celery import group
from django.core.files.base import ContentFile

from django.db.models import QuerySet

from .models import Printer, Check
from .tasks import generate_check


def is_printers_at_point_exists(point_id: int) -> bool:
    """
    Check if there are printers with this point_id in db.
    """
    return Printer.objects.filter(point_id=point_id).exists()


def is_checks_with_order_id_exists(order_id: int) -> bool:
    """
    Check if there are checks with this order_id in db.
    """
    return Check.objects.filter(order__order_id=order_id).exists()


def bulk_create_checks(printers: QuerySet[Printer], order: dict) -> None:
    """
    Bulk create Checks for every printer.
    """
    Check.objects.bulk_create([
        Check(
            printer=printer, type=printer.check_type, order=order
        ) for printer in printers
    ])


def create_checks_at_point(point_id: int, order_id: int, order: dict) -> None:
    """
    Create Checks with PDF file for every printer at a point.
    """
    printers = Printer.objects.filter(point_id=point_id).only('check_type')
    bulk_create_checks(printers, order)
    group([
        generate_check.s(
            order, order_id, printer.check_type, printer.pk
        ) for printer in printers
    ])()


def get_rendered_checks_at_point(point: str) -> QuerySet[Check]:
    """
    Get all Checks with status='RENDERED' at a `point`
    with needed for printer device fields.
    """
    return Check.objects.filter(
        printer__point_id=point, status='RENDERED'
    ).select_related('printer').only('printer', 'type', 'pdf_file')


def update_check_to_rendered(
    printer_pk: str, order_id: int, content_file: ContentFile
) -> None:
    """
    Update the status and PDF file of a Check based
    on the given `printer_pk` and `order_id`.
    """
    check = Check.objects.filter(
        printer_id=printer_pk, order__order_id=order_id
    ).only('id').get()
    check.status = 'RENDERED'
    check.pdf_file = content_file
    check.save()
