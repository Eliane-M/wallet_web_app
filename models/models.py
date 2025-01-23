from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    last_transaction_type = models.CharField(max_length=255, blank=True, null=True)
    last_transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return self.name, self.account_type
    
class AccountDetails(models.Model):
    ACCOUNT_TYPE = [
        ('bank_account', 'bank_account'),
        ('momo_account', 'momo_account'),
        ('cash', 'cash'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, default=None)
    account = models.OneToOneField(Wallet, on_delete=models.CASCADE, null=True, blank=True)
    # account_id = models.UUIDField(null=True, blank=True)
    account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    # For Bank account
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    # For Mobile money
    phone_number = models.IntegerField(blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)
    # Card details
    card_number = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Details for {self.account.name}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer_sent', 'Transfer_sent'),
        ('Transfer_received', 'Transfer_received'),
    ]

    STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, null=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=255, null=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS, max_length=255)
    description = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return self.transaction_amount
    
class PaymentMethod(models.Model):
    METHODS = [
        ('Bank', 'Bank Transfer'),
        ('Card', 'Debit/Credit Card'),
        ('Momo', 'Momo Pay'),
    ]

    account = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(choices=METHODS, max_length=255)
    title = models.CharField(max_length=255)
    # For bank transfer
    account_number = models.CharField(max_length=255)
    account_holder_name = models.CharField(max_length=255)
    # For credit/debit card
    card_number = models.CharField(max_length=255)
    expiration_date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    # For momo pay
    momo_number = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TransactionCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=500)
    icon = models.ImageField(upload_to='transaction_categories/', blank=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class TransactionTag(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='tags')
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['transaction', 'category']

    def __str__(self):
        return f"{self.category} - {self.transaction}"