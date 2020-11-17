import os

from celery import shared_task

from config.settings import BASE_DIR
from .models import Order
from django.http import request, HttpResponse
import pydf


@shared_task
def create_pdf(request):
    order_id = request.GET.get('id')
    order = Order.objects.get(pk=order_id)
    order_html = order.generate_html()
    pdf = pydf.generate_pdf(order_html, encoding='utf-8')
    output_filename = os.path.join(BASE_DIR, 'pdf/checkout.pdf')
    with open(output_filename, 'wb') as f:
        f.write(pdf)
    with open(output_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read())
        response['Content-Type'] = 'mimetype/submimetype'
        response['Content-Disposition'] = 'attachment; filename=regulation.pdf'
    return response

