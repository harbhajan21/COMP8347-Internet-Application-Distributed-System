from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


# Create your models here
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
