from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [

    path('rest_list/', views.RestaurantList.as_view(),name='rest_list'),
    path('top_rests/', views.TopRestaurants.as_view(),name='top_rests'),
    path('rest_detail/<int:pk>', views.RestaurantDetail.as_view(),name='rest_detail'),
    path('dish_list/', views.DishList.as_view(),name='dish_list'),
    path('dish_detail/<int:pk>', views.DishDetail.as_view()),
    path('top_dishes/', views.TopDishes.as_view(), name='top_dishes'),
    path('rest_review_list/<int:pk>',views.RestaurantReviewList.as_view()),
    path('current_user/',views.current_user,name='current_user'),
    path('rest_review_detai/<int:pk>',views.RestaurantReviewDetail.as_view()),
    path('dish_review_list/<int:pk>', views.DishReviewList.as_view()),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('order_list/', views.OrderList.as_view()),
    path('order_detail/<int:pk>', views.OrderDetail.as_view()),
    path('dishes_of_rest/<int:pk>',views.DishesOfRestaurant.as_view(),name='dishes_of_rest'),
    path('top_dishes_of_rest/<int:pk>', views.DishesOfRestaurant.as_view(), name='top_dishes_of_rest'),
    path('search_rest/', views.SearchRestaurant.as_view(),name='search_rest'),
    path('search_dish/<slug:rname>', views.SearchDish.as_view()),
    path('', views.home,name='home'),
    path('newlogin/', views.mynewlogin, name='newlogin'),
    path('newregister/', views.mynewregister, name='newregister'),
    path('newlogout/', views.logout, name='newlogout'),
    path('success/', views.success, name='success'),
    path('get_category/<slug:rname>',views.GetDishesByCategory.as_view(),name='get_category')

]

