"""
Adds simple form view, which communicates with Braintree.
There are four steps to finally process a transaction:
1. Create a client token (views.py)
2. Send it to Braintree (js)
3. Receive a payment nonce from Braintree (js)
4. Send transaction details and payment nonce to Braintree (views.py)
"""
import braintree
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from . import forms
from .mixins import LoginRequiredMixin



class CheckoutView(LoginRequiredMixin, FormView):
    """This view lets the user initiate a payment."""
    form_class = forms.CheckoutForm
    template_name = 'shop/payment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['amount'] = Decimal('12.55')
        kwargs['invnum'] = 'BA1234'
        kwargs['currency'] = 'GBP',
        
        return kwargs

    def form_valid(self, form):
        form.process(self.request)
        return super(CheckoutView, self).form_valid(form)

    def get_success_url(self):
        return reverse('checkout')
    

