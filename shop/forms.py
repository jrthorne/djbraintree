"""
Add a simple form, which includes the hidden payment nonce field.
You might want to add other fields like an address, quantity or
an amount.
"""
import braintree
from django import forms
from django.conf import settings
from django_enumfield import enum
from django.utils.translation import ugettext_lazy as _
import uuid

class InstallmentTypes(enum.Enum):
    FULL = 1
    DEPOSIT = 2
    BALANCE = 3

    labels = {
        FULL: 'Full',
        DEPOSIT: 'Deposit', 
        BALANCE: 'Balance'
    }

class CheckoutForm(forms.Form):

    payment_method_nonce = forms.CharField(
        max_length=1000,
        widget=forms.widgets.HiddenInput,
        required=False,
    )
    amount = forms.DecimalField(required=True)
    installment = forms.ChoiceField(widget=forms.RadioSelect, choices=InstallmentTypes.choices(), required=True)

    def __init__(self, *args, **kwargs):

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox
            
        # Configure Braintree
        braintree_config = braintree.Configuration(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
        self.gateway = braintree.BraintreeGateway(braintree_config)
        self.braintree_client_token = self.gateway.client_token.generate({})

        self.co_params = {}
        amount = kwargs.pop('amount', None)
        self.invnum = kwargs.pop('invnum', None)
        currency = kwargs.pop('currency', None)
        retval = super().__init__(*args, **kwargs)
        self.initial['installment'] = InstallmentTypes.FULL # default
        self.initial['amount'] = amount
        return retval

    def process(self, request, guest=None):
        self.co_params['ipaddress'] = request.META.get("REMOTE_ADDR", "")
        result = self.gateway.transaction.sale({
            "amount": self.cleaned_data['amount'],
            'order_id': self.invnum,
            'custom_fields': {
                'confirmation_codes': self.invnum,
                'transaction_uuid': str(uuid.uuid4)
            },
            'payment_method_nonce': self.cleaned_data['payment_method_nonce'],
            'options': {
                'submit_for_settlement': True,
            },
        })
        if not result.is_success:
            self.co_params['flag'] = True
            self.co_params['message'] = 'Your payment could not be processed. Please check your input or use another payment method and try again.'
        else:
            self.co_params['transaction_id'] = result.transaction.id
        return self.co_params
    
    def clean(self):
        self.cleaned_data = super(CheckoutForm, self).clean()
        if not self.cleaned_data.get('payment_method_nonce'):
            raise forms.ValidationError(_(
                'We couldn\'t verify your payment. Please try again.'))
        return self.cleaned_data