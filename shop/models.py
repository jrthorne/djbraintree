from django.db import models
import uuid

class Transaction(models.Model):
    transaction_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    desc = models.TextField(blank=True)
    method = models.PositiveIntegerField(choices=TransactionTypes.choices(), default=TransactionTypes.CREDIT)
    currency = models.CharField(max_length=3, default='GBP', choices=settings.CURRENCY_CHOICES)
    card_name = models.CharField(max_length=72, blank=True)
    card_type = models.CharField(max_length=12, blank=True)
    card_four = models.CharField(max_length=4, blank=True)
    transaction_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    txn_id = models.CharField(max_length=72, blank=True, null=True)
    installment = models.PositiveIntegerField(choices=InstallmentTypes.choices(), default=InstallmentTypes.FULL)

    class Meta(object):
        ordering = [ '-created' ]

    def __str__(self):
        return '%.2f %s [%s#%s]' % ( self.amount, self.currency, self.method, self.booking_references_display )

