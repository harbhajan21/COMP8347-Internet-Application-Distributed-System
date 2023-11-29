from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    today_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class FearAndGreedIndex(models.Model):
    date = models.DateField()
    value = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.value}'


class News(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()

    def __str__(self):
        return self.title


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    user_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    payment_option = models.CharField(max_length=10)
    transaction_date = models.DateTimeField(default=timezone.now)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment by {self.user_name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    coin_symbol = models.CharField(max_length=10)
    coin_name = models.CharField(max_length=100)
    price_per_coin = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.coin_symbol} by {self.payment.user.username}"

    def save(self, *args, **kwargs):
        # Convert to Decimal before arithmetic operation
        price_per_coin = Decimal(str(self.price_per_coin))
        quantity = Decimal(str(self.quantity))
        if self.transaction_type == 'BUY':
            required_balance = price_per_coin * quantity
            current_balance = self.payment.account_balance

            if required_balance > current_balance:
                raise ValidationError("Not enough account balance. Add funds.")
            else:
                # Deduct the amount from the payment's account balance and save
                self.payment.account_balance -= required_balance
                self.payment.save()
                super().save(*args, **kwargs)
        elif self.transaction_type == 'SELL':
            print("inside sell logic")
            # Add the logic for selling coins
            sold_amount = price_per_coin * quantity
            self.payment.account_balance += sold_amount
            self.payment.save()
            super().save(*args, **kwargs)
