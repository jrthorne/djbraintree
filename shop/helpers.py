from django_enumfield import enum
from django import forms

class InstallmentTypes(enum.Enum):
    FULL = 1
    DEPOSIT = 2
    BALANCE = 3

    labels = {
        FULL: 'Full',
        DEPOSIT: 'Deposit', 
        BALANCE: 'Balance'
    }

class TransactionTypes(enum.Enum):
    """
    Other than FAKE, these mirror the payment types defined on Dojo's 
    money.models.Payment class
    """
    FAKE = 0
    PAYPAL = 4
    CREDIT = 6
    INTROCART_REST = 9
    
    labels = {
        FAKE: 'Fake',
        PAYPAL: 'Paypal',
        CREDIT: 'Credit',
        INTROCART_REST: 'DOJO Only'
    }
