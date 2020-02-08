from django.urls import path

import orders.driver_view
from . import views
from . import driver_view

app_name = 'orders'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('request_ride/', views.RequestRideView.as_view(), name='request_ride'),
    path('<int:pk>/modify_ride/', views.ModifyRideView.as_view(), name='modify_ride'),

    path('<int:pk>/confirm_ride/', orders.driver_view.ConfirmRideView.as_view(), name='confirm_ride'),
    path('my_ride/', views.MyRideView.as_view(), name='my_ride_list'),
    path('<int:pk>/ride_detail_rider/', views.RideDetailView.as_view(), name='ride_detail'),

    path('check_ride_rider/', views.CheckRideViewRider.as_view(), name='check_ride_rider'),
    path('check_order_driver/', driver_view.CheckOrderViewDriver.as_view(), name='check_order_driver'),
    path('check_my_ride_driver/', driver_view.CheckMyOrderViewDriver.as_view(), name='check_my_order_driver'),
    path('menu_rider/', views.MenuViewRider.as_view(), name='menu_rider'),
    path('menu_driver/', views.MenuViewDriver.as_view(), name='menu_driver'),
    path('join_ride_search/', views.JoinRideSearchView.as_view(), name='join_ride_search'),
    path('join_ride_list/', views.JoinRideListView.as_view(), name='join_ride_list'),
    path('<int:pk>/join_ride/', views.JoinRideView.as_view(), name='join_ride'),
    path('modify_failed/', views.ModifyFailView.as_view(), name='modify_fail'),
    path('join_ride_failed/', views.JoinRideFailView.as_view(), name='join_fail')
]

