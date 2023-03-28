from django.contrib import admin

from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')
    search_fields = ('name', 'api_key')
    save_on_top = True
    save_as = True


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer', 'type', 'status')
    save_on_top = True
    save_as = True
    list_filter = ('printer', 'type', 'status')
    exclude = ('pdf_file',)
