from django.http import Http404
from django.db.models import FloatField
from django.db.models import Avg
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from main.serializers import *
from main.models import Restaurant,Dish,DishReview,RestaurantReview
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from main.forms import *
 

class RestaurantList(APIView):
    pagination_class = (PageNumberPagination,)
    def get(self, request):
        rests = Restaurant.objects.all()
        context={'rests':rests}
        return render(request,'rest_list.html',context)


class RestaurantDetail(APIView):

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        rest = self.get_object(pk)
        stars_map = rest.restaurant_reviews.all().aggregate(Avg('stars'))
        stars1 = stars_map.get('stars__avg')

        if stars1 is not None:
            stars = int(stars1)
            remainder = abs(5 - stars)
            if (remainder < 1):
                remainder = 0
        else:
            stars = 0
            remainder = 5
        return render(request,'rest_detail.html',{'rest':rest,'stars':range(stars), 'remainder':range(remainder)})


class DishList(APIView):

    def get(self, request):
        dishes = Dish.objects.all()

        return render(request,'dish_list.html',{'dishes':dishes})


class DishDetail(APIView):

    def get_object(self, pk):
        try:
            return Dish.objects.get(id=pk)
        except Dish.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dish = self.get_object(pk)
        stars_map= dish.dishes_reviews.all().aggregate(Avg('stars'))
        stars1 = stars_map.get('stars__avg')

        if stars1 is not None:
            stars = int(stars1)
            remainder = abs(5-stars)
            if(remainder<1):
                remainder=0
        else:
            stars=0
            remainder=5
        return render(request, 'dish_detail.html', {'dish':dish,'stars':range(stars),'remainder':range(remainder)})






class RestaurantReviewList(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404
    def get(self, request,pk):
        restaurant=self.get_object(pk)
        rest_reviews = restaurant.restaurant_reviews.all()
        serializer = RestaurantReviewModelSerializer(rest_reviews, many=True)
        return Response(serializer.data)

    def post(self, request,pk):
        rest=self.get_object(pk)
        serializer = RestaurantReviewModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant = rest,user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantReviewDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return RestaurantReview.objects.get(id=pk)
        except RestaurantReview.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        rest_review = self.get_object(pk)
        serializer = RestaurantReviewModelSerializer(rest_review)
        return Response(serializer.data)

    def put(self, request, pk):
        rest_review = self.get_object(pk)
        serializer = RestaurantReviewModelSerializer(instance=rest_review, data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rest_review = self.get_object(pk)
        rest_review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class DishReviewList(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Dish.objects.get(id=pk)
        except Dish.DoesNotExist:
            raise Http404
    def get(self, request,pk):
        dish = self.get_object(pk)
        dish_reviews = dish.dishes_reviews.all()
        serializer = DishReviewModelSerializer(dish_reviews,many=True)
        return Response(serializer.data)

    def post(self, request,pk):
        curdish = self.get_object(pk)
        serializer = DishReviewModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user,dish=curdish)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Checkout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):

        items=request.POST.get('items')
        product_string=items.split(';')
        product_string=product_string[:-1]
        price =0
        order = Order()
        order.owner=request.user
        order.save()
        for product in product_string:
            product_fields=product.split(',')
            for j in range(int(product_fields[2])):
                order_item=OrderItem()
                dish = Dish.objects.get(name=product_fields[1])
                order_item.dish=dish
                order_item.order=order
                price+=int(product_fields[0])
                order_item.save()
        order.price=price
        order.save()
        context = {
            'order':order
        }
        return render(request,'checkout.html',context)

class OrderList(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request):
        order = Order.objects.filter(owner = request.user)
        serializer = OrderModelSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = OrderModelSerializer(data=request.data,context={'items': request.data.get('items')})
        if serializer.is_valid():

            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderModelSerializer(order)
        return Response(serializer.data)


    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DishesOfRestaurant(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        rest_dishes = restaurant.dishes.all()
        context={'dishes':rest_dishes}
        return render(request,'dish_of_rest.html',context)

class TopDishesOfRestaurant(APIView):
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        restaurant = self.get_object(pk)
        rest_dishes = restaurant.dishes.all()
        sorted_dishes = rest_dishes.order_by('num_of_orders')
        context={'dishes':sorted_dishes}
        return render(request,'dish_of_rest.html',context)


class TopRestaurants(APIView):
    def get(self, request):

        rests_all = Restaurant.objects.all()
        rests = rests_all.annotate(count=Count('restaurant_reviews')).order_by('-count')
        context={'rests':rests}
        return render(request,'rest_list.html',context)

class TopDishes(APIView):
    def get(self, request):

        dishes_all = Dish.objects.all()
        dishes =  dishes_all.annotate(count=Count('dishes_reviews')).order_by('-count')
        context={'dishes': dishes}
        return render(request, 'dish_list.html', context)

class SearchRestaurant(APIView):

    def get_query(self):
        search_query = self.request.GET.get('search_box')
        print(search_query)
        rests = Restaurant.objects.filter(name__contains=search_query)
        return rests

    def get(self, request):

        rests = self.get_query(self)

        serializer = RestaurantModelSerializer(rests,many=True)
        return Response(serializer.data)
        #return render(serializer)
class SearchDish(APIView):

    def get_queryset(self,rname):
        try:
            return Dish.objects.filter(name__contains=rname)
        except Dish.DoesNotExist:
            raise Http404
    def get(self, request,rname):
        rests = self.get_queryset(rname)
        serializer = DishModelSerializer(rests,many=True)
        return Response(serializer.data)
class GetDishesByCategory(APIView):
    def get_queryset(self,rname):
        try:
            return Dish.objects.filter(category=rname)
        except Dish.DoesNotExist:
            raise Http404
    def get(self, request,rname):
        dishes = self.get_queryset(rname)
        context={'dishes':dishes}
        return render(request,'dish_list.html',context)
class SearchDish(APIView):

    def get_queryset(self,rname):
        try:
            return Dish.objects.filter(name__contains=rname)
        except Dish.DoesNotExist:
            raise Http404
    def get(self, request,rname):
        rests = self.get_queryset(rname)
        serializer = DishModelSerializer(rests,many=True)
        return Response(serializer.data)