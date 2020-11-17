import os

from celery import shared_task

from config.settings import BASE_DIR
from .models import Order
from django.http import request, HttpResponse
from weasyprint import HTML
import pdfkit


@shared_task
def create_pdf(request):
    options = {
        'encoding': "UTF-8",
    }

    order_id = request.GET.get('id')
    order = Order.objects.get(pk=order_id)
    order_html = order.generate_html()
    pdfkit.from_string(order_html, 'pdf/checkout.pdf', options=options)
    output_filename = os.path.join(BASE_DIR, 'pdf/checkout.pdf')
    with open(output_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read())
        response['Content-Type'] = 'mimetype/submimetype'
        response['Content-Disposition'] = 'attachment; filename=regulation.pdf'
    return response

