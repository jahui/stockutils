from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DEFAULT_USER = 1
class Trade(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER)
	ticker = models.CharField(max_length=10)
	price = models.DecimalField(max_digits=11, decimal_places=2)
	trade_date = models.DateField()
	shares = models.IntegerField(default=0)
	# a negative amount means a sale

	#trade_type = models.BooleanField(default=None)
	# true = buy, false = sell

	def __str__(self):
		return self.ticker