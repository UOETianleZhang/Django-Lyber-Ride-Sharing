from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from Lyber import settings
from .models import Choice, Question, Ride, RiderSharer
from .forms import RiderDriverForm, RideForm, RiderDriver, Order

from django.contrib.auth.mixins import LoginRequiredMixin


def getDriverByRequest(request):
    return RiderDriver.objects.get(user=request.user)


@login_required()
def driver_page_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    # request, template name, context info
    print(request)
    return render(request, "driverPage.html", {})


def driver_open_order_list_view(request):
    queryset = Ride.objects.all().filter()  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "products/product_list.html", context)


def driver_order_detail_view(request, id):
    obj = get_object_or_404(RiderDriver, id=id)
    context = {
        "object": obj
    }
    return render(request, "products/product_detail.html", context)


class CheckOrderViewDriver(LoginRequiredMixin, generic.ListView):
    template_name = 'driver/check_order_driver.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        order_list = []
        driver = getDriverByRequest(self.request)
        for order in Order.objects.all():
            if order.ride.status == 'open' \
                    and (order.ride.owner_passenger_num is None or order.ride.owner_passenger_num <= driver.max_passenger_num) \
                    and (order.ride.vehicle_type is None or order.ride.vehicle_type == driver.vehicle_type) \
                    and (order.ride.special_request == driver.special_info or order.ride.special_request == 0
                         or order.ride.special_request is None):
                order_list.append(order)
        return order_list


class CheckMyOrderViewDriver(LoginRequiredMixin, generic.ListView):
    template_name = 'driver/check_order_driver.html'
    context_object_name = 'latest_ride_list'
    form_class = RideForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        return Order.objects.filter(driver=getDriverByRequest(self.request))


#################
class ModifyOrderView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/modify_ride.html'
    model = Ride
    fields = '__all__'
    context_object_name = 'ride'

    def get_success_url(self):
        return reverse('orders:check_ride')


def confirm(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.status = 'confirmed'
    ride.save()
    return HttpResponseRedirect(reverse('orders:ride_detail', args=(ride.id)))

class ConfirmRideView(LoginRequiredMixin, generic.UpdateView):
    model = Ride
    fields = '__all__'
    template_name = 'driver/confirm_ride_order_version.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        driver = getDriverByRequest(self.request)
        sharerList = RiderSharer.objects.filter(order__driver_id__exact=order.id)
        sharers = []
        for s in sharerList:
            sharers.append(s)
        driver.user.first_name
        context['ride'] = ride
        context['driver'] = driver
        context['sharers'] = sharers
        context['order'] = order
        context['owner'] = order.owner
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        driver = getDriverByRequest(request)

        if 'confirm' in request.POST:
            if (not ride.status == 'open') or (driver.is_driving is True):
                # TODO: error handling, stop
                return render(request, self.template_name, {'ride': ride, 'error': "Cannot confirm the order! Might "
                                                                                   "because the driver is driving or "
                                                                                   "the order is not open anymore.",
                                                            'driver': driver})
            email = [order.user.email for order in order.ridersharer_set.all()]
            email = email + [order.owner.email, driver.user.email]
            send_mail('The Order is Comfirmed!',
                      'The driver is on the way. Enjoy your ride!\nPlease rate our service: ☆☆☆☆☆\n', settings.EMAIL_FROM,
                      email, fail_silently=False)
            ride.status = 'confirmed'
            Ride.special_request = driver.special_info
            Ride.max_passenger_num = driver.max_passenger_num
            Ride.vehicle_type = driver.vehicle_type
            driver.is_driving = True
            order.driver = driver
            driver.save()
            ride.save()
            order.save()
            return super().post(request, *args, **kwargs)

        elif 'finish' in request.POST:
            ride.status = 'finish'
            driver.is_driving = False
            ride.save()
            order.save()
            driver.save()
            # send email
            return redirect("orders:menu_driver")
        else:
            pass
