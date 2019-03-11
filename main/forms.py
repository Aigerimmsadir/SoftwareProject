from django.forms import ModelForm
from .models import *


class RestaurantForm(ModelForm):
	class Meta:
		model = Restaurant
		fields=('name','address')
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ('price',)