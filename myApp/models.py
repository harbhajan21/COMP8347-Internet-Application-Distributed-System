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
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    card_number = models.CharField(max_length=16)
    user_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    payment_option = models.CharField(max_length=10)
    transaction_date = models.DateTimeField(default=timezone.now)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment by {self.user_name}"
