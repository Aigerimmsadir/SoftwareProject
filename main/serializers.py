from rest_framework import serializers
from main.models import Restaurant,Dish,Review,RestaurantReview,DishReview,Order,OrderItem
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator
import datetime
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework import status

class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class RestaurantModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)



    class Meta:
        model = Restaurant
        fields = ['name','address',]

    def create(self, validated_data):


        rest = Restaurant.objects.create(**validated_data)
        print(validated_data)
        rest.save()
        return rest
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
class DishModelSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=100)
    restaurant=RestaurantModelSerializer()
    description =serializers.CharField(max_length=1000)
    price =serializers.IntegerField()
    class Meta:
        model = Dish
        fields = ['name','restaurant','description','price']


    def create(self, validated_data):
        tracks_data = validated_data.pop('restaurant')
        restaurant = Restaurant.objects.get(name = tracks_data.get('name'))
        print(restaurant)
        dish = Dish.objects.create(restaurant=restaurant, **validated_data)
        # dish=Dish(**validated_data)
        # dish.restaurant=Restaurant.objects.first()
        print(validated_data)
        dish.save()
        return dish
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
class ReviewModelSerializer(serializers.ModelSerializer):

    comment = serializers.CharField(max_length=1000)
    date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Review
        fields = ['comment','date']


    def create(self, validated_data):
        review=Review(**validated_data)
        print(validated_data)
        review.save()
        return review
    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)

        instance.save()
        return instance


class RestaurantReviewModelSerializer(serializers.ModelSerializer):

    restaurant = RestaurantModelSerializer()
    user = UserModelSerializer(read_only=True)
    review=ReviewModelSerializer()

    class Meta:
        model = RestaurantReview
        fields = ['id','restaurant','user', 'review']


    def create(self, validated_data):
        tracks_data = validated_data.pop('restaurant')
        #restaurant = Restaurant.objects.get(name = tracks_data.get('name'))

        review_data = validated_data.pop('review')
        review = Review.objects.create(comment=review_data.get('comment'))

        restReview = RestaurantReview.objects.create(review=review,**validated_data)
        
        restReview.save()
        return restReview
    def update(self, instance, validated_data):

        tracks_data = validated_data.pop('restaurant')
        restaurant = Restaurant.objects.get(name=tracks_data.get('name'))

        review_data = validated_data.pop('review')
        review = Review.objects.create(comment=review_data.get('comment'))
        instance.restaurant=restaurant
        instance.review = review
        instance.save()
        return instance



class DishReviewModelSerializer(serializers.ModelSerializer):

    dish = DishModelSerializer()
    user = UserModelSerializer(read_only=True)
    review=ReviewModelSerializer()

    class Meta:
        model = DishReview
        fields = ['dish','user', 'review']


    def create(self, validated_data):
        tracks_data = validated_data.pop('dish')
        #dish = Dish.objects.get(name = tracks_data.get('name'))

        review_data = validated_data.pop('review')
        review = Review.objects.create(comment=review_data.get('comment'))

        dishReview = DishReview.objects.create(review=review,**validated_data)#dish=dish

        dishReview.save()
        return dishReview
    def update(self, instance, validated_data):

        tracks_data = validated_data.pop('dish')
        dish = Dish.objects.get(name=tracks_data.get('name'))

        review_data = validated_data.pop('review')
        review = Review.objects.create(comment=review_data.get('comment'))
        instance.dish = dish
        instance.review = review
        instance.save()
        return instance


class OrderModelSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    price = serializers.IntegerField(default=0)

    owner = UserModelSerializer(read_only=True)


    class Meta:
        model = Order
        fields = [ 'date', 'price', 'owner']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)

        #creating items of order
        items = self.context.get("items")

        for i in items:
            dish = Dish.objects.get(name =i)
            dish.num_of_orders+=1
            order.price+=dish.price*1.1
            item = OrderItem.objects.create(dish=dish, order=order)
        if(order.price!=0):
            order.save()
            return order
        else:
            order.delete()

            return order


