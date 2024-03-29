import json

import stripe
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from ..order.models import Order
from ..order.views import render_to_pdf


@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeded':
        payment_intent = event.data.object

        print('Payment intent: ', payment_intent.id)

        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True
        order.save()

        for item in order.items.all():
            product = item.product
            product.num_available = product.num_available - item.quantity
            product.save()

        subject = 'Order confirmation'
        from_email = 'noreply@ecommerce.com'
        to = ['mail@ecommerce.com', order.email]
        text_content = 'Your order is successful!'
        html_content = render_to_string('order_confirmation.html', {'order': order})

        pdf = render_to_pdf('order_pdf.html', {'order': order})

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        if pdf:
            name = f'order_{order.id}.pdf'
            msg.attach(name, pdf, 'application/pdf')

        msg.send()

        # html = render_to_string('order_confirmation.html', {'order': order})
        # send_mail('Order confirmation', 'Your order is successful!', 'noreply@ecommerce.com',
        #           ['mail@ecommerce.com', order.email], fail_silently=True, html_message=html)

    return HttpResponse(status=200)
