from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Order


def render_to_pdf(template_src, context_dict=None):
    template = get_template(template_src)
    if context_dict is None:
        context_dict = {}

    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-2")), result)

    if not pdf.err:
        return result.getvalue()

    return None


@login_required
def admin_order_pdf(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, pk=order_id)
        pdf = render_to_pdf('order_pdf.html', {'order': order})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            content = f"attachment; filename={order_id}.pdf"
            response['Content-Disposition'] = content

            return response

    return HttpResponse("Not found")
