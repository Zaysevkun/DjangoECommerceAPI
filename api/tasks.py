import os

from celery import shared_task
from django.conf.global_settings import STATIC_ROOT
from .models import Order
from django.http import request, HttpResponse
from weasyprint import HTML
import pdfkit


@shared_task
def create_pdf(request):
    order_id = request.GET.get('id')
    order = Order.objects.get(pk=order_id)
    order_html = order.generate_html()
    pdfkit.from_string(order_html, 'pdf/checkout.pdf')
    output_filename = os.path.join(STATIC_ROOT, 'pdf/checkout.pdf')
    with open(output_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read())
        response['Content-Type'] = 'mimetype/submimetype'
        response['Content-Disposition'] = 'attachment; filename=regulation.pdf'
    return response

