from django.forms import ModelForm
from .models import Restaurant,Dish, Review, RestaurantReview,DishReview


class RestaurantForm(ModelForm):
	class Meta:
		model = Restaurant
		fields=('name','address')
			
				
