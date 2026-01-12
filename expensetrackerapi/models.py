from django.db import models
from django.contrib.auth.models import AbstractUser
from django_project import settings
from djmoney.models.fields import MoneyField

class Category(models.TextChoices):
    GROCERIES = 'Groceries', 'Groceries'
    LEISURE = 'Leisure', 'Leisure'
    ELECTRONICS = 'Electronics', 'Electronics'
    UTILITIES = 'Utilities', 'Utilities'
    CLOTHING = 'Clothing', 'Clothing'
    HEALTH = 'Health', 'Health'
    OTHERS = 'Others', 'Others'

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Expenses(models.Model):
    description = models.CharField()
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date = models.DateTimeField()
    category = models.CharField(
        max_length=20,
        choices=Category,
        default=Category.OTHERS
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )