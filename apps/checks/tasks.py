import base64
import json

import requests
from celery import shared_task

from django.core.files.base import ContentFile
from django.template.loader import render_to_string


@shared_task()
def generate_check(
    order: dict, order_id: int, check_type: str, printer_pk: str
) -> None:
    """
    Create pdf file of an order for Check from html template.
    """
    from .services import update_check_to_rendered

    url = 'http://0.0.0.0:80/'
    template_name = 'check_template.html'
    context = order
    template_content = render_to_string(template_name, context).encode('utf-8')
    data = {'contents': base64.b64encode(template_content).decode('utf-8')}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    file_name = f'{order_id}_{check_type}.pdf'
    content_file = ContentFile(response.content, name=file_name)
    update_check_to_rendered(printer_pk, order_id, content_file)
