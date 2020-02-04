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
    path('<int:pk>/ride_detail_driver/', driver_view.OrderDetailView.as_view(), name='ride_detail'),
    path('my_ride/', views.MyRideView.as_view(), name='my_ride_list'),
    path('<int:pk>/ride_detail_rider/', views.RideDetailView.as_view(), name='ride_detail'),

    path('check_ride_rider/', views.CheckRideViewRider.as_view(), name='check_ride_rider'),
    path('check_order_driver/', driver_view.CheckOrderViewDriver.as_view(), name='check_order_driver'),
    path('check_my_ride_driver/', driver_view.CheckMyOrderViewDriver.as_view(), name='check_my_order_driver'),
    path('menu_rider/', views.MenuViewRider.as_view(), name='menu_rider'),
    path('menu_driver/', views.MenuViewDriver.as_view(), name='menu_driver'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('join_ride_search/', views.JoinRideSearchView.as_view(), name='join_ride_search'),
    path('join_ride_list/', views.JoinRideListView.as_view(), name='join_ride_list'),
    path('<int:pk>/join_ride/', views.JoinRideView.as_view(), name='join_ride'),
    path('modify_failed/', views.ModifyFailView.as_view(), name='modify_fail')
    # path('<int:ride_id>/confirm/', views.confirm, name='confirm'),
]

# from django.contrib import admin
# from django.urls import path
# # Use include() to add URLS from the catalog application and authentication system
# from django.urls import include
# from orders.views import signup_view, user_page_view, home_view, driver_page_view
#
# urlpatterns = [
#     path('', home_view, name='home'),
#     path('admin/', admin.site.urls),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('signup/', signup_view, name='signUp'),
#     path('userPage/', user_page_view, name='userPage'),
#     path('driverPage/', driver_page_view , name='driverPage')
# ]