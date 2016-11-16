from django.db import models

# Create your models here.
class Trade(models.Model):
	ticker = models.CharField(max_length=10)
	price_bought = models.DecimalField(max_digits=11, decimal_places=2)
	date_bought = models.DateTimeField()
	price_sold = models.DecimalField(max_digits=11, decimal_places=2)
	date_sold = models.DateTimeField()