from django.db import models

CHECK_TYPES = (
    ('KITCHEN', 'kitchen'),
    ('CLIENT', 'client'),
)


class Printer(models.Model):
    """
    Represents a printer device.
    """
    name = models.CharField('Printer name', max_length=255)
    api_key = models.CharField(
        'Access key to API', primary_key=True,
        max_length=255, unique=True, blank=True
    )
    check_type = models.CharField(
        'Check type that the printer device prints',
        max_length=7, choices=CHECK_TYPES
    )
    point_id = models.PositiveSmallIntegerField(
        'Point to which the printer is bound')

    class Meta:
        db_table = 'printer'

    def __str__(self) -> str:
        return str(self.name)


class Check(models.Model):
    """
    Represents a receipt or bill.
    """
    STATUSES = (
        ('NEW', 'new'),
        ('RENDERED', 'rendered'),
        ('PRINTED', 'printed'),
    )

    printer = models.ForeignKey(
        Printer, on_delete=models.CASCADE, verbose_name='Printer device')
    type = models.CharField('Check type', max_length=7, choices=CHECK_TYPES)
    order = models.JSONField('Order information')
    status = models.CharField(
        'Check status', max_length=8, choices=STATUSES, default='NEW')
    pdf_file = models.FileField(
        'Link to the generated PDF file', upload_to='media/pdf', null=True)

    class Meta:
        db_table = 'check'

    def __str__(self) -> str:
        return str(self.pk)
