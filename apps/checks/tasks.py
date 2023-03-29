import subprocess

from celery import shared_task

from django.conf import settings
from django.core.files.base import ContentFile

from .models import Check


@shared_task()
def generate_check(
    order_id: int, check_type: str, printer_pk: str
) -> None:
    """
    Create pdf file of an order for Check from html template.
    """
    template_path = str(settings.BASE_DIR / 'templates/check_template.html')
    file_name = f'{order_id}_{check_type}.pdf'
    command = ['wkhtmltopdf', template_path, '-']
    pdf_output = subprocess.run(command, stdout=subprocess.PIPE)
    content_file = ContentFile(pdf_output.stdout, name=file_name)
    check = Check.objects.get(printer_id=printer_pk, order__order_id=order_id)
    check.pdf_file = content_file
    check.save()
