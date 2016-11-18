from django.db import models

# Create your models here.
class Trade(models.Model):
	ticker = models.CharField(max_length=10)
	price = models.DecimalField(max_digits=11, decimal_places=2)
	trade_date = models.DateField()
	shares = models.IntegerField(default=0)
	# a negative amount means a sale

	#trade_type = models.BooleanField(default=None)
	# true = buy, false = sell

	def __str__(self):
		return self.ticker