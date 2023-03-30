import base64
import json

import requests
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
    url = 'http://0.0.0.0:80/'
    template_path = str(settings.BASE_DIR / 'templates/check_template.html')
    data = {
        'contents': base64.b64encode(
            open(template_path, 'rb').read()
        ).decode('utf-8')
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    file_name = f'{order_id}_{check_type}.pdf'
    content_file = ContentFile(response.content, name=file_name)
    check = Check.objects.get(printer_id=printer_pk, order__order_id=order_id)
    check.status = 'RENDERED'
    check.pdf_file = content_file
    check.save()
