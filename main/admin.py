from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(ImageRest)
admin.site.register(ImageDish)
admin.site.register(Order)
admin.site.register,(OrderItem)
admin.site.register(Dish)
admin.site.register(Review)
admin.site.register(RestaurantReview)
admin.site.register(DishReview)