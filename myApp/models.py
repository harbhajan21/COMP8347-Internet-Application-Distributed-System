from django.db import models
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


# Create your models here.
class Payment(models.Model):
    amount = models.CharField(max_length=10)
    card_number = models.CharField(max_length=16)
    user_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    payment_option = models.CharField(max_length=10)

    def __str__(self):
        return f"Payment by {self.user_name}"