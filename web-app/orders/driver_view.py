from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Ride
from .models import RideForm, RiderDriver, Order
from .forms import RiderDriverForm

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
    queryset = Ride.objects.all().filter() # list of objects
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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        order_list = []
        for order in Order.objects.all():
            if order.ride.status == 'open':
                order_list.append(order)
        return order_list

class CheckMyOrderViewDriver(LoginRequiredMixin, generic.ListView):
    template_name = 'driver/check_order_driver.html'
    context_object_name = 'latest_ride_list'
    form_class = RideForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        """Return the last five published questions."""
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
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('orders:ride_detail', args=(ride.id)))


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ride
    template_name = 'driver/confirm_ride_order_version.html'
    toFinish = True

    def get(self, request, *args, **kwargs):
        error = []
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        driver = getDriverByRequest(request)
        return render(request, self.template_name, {'ride' : ride, 'error' : error, 'toFinish' : self.toFinish})

    def post(self, request, *args, **kwargs):
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        ride.status = 'finish'
        ride.save()
        order.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return redirect(reverse('orders:ride_detail', args=[ride.id]))

class ConfirmRideView(LoginRequiredMixin, generic.DeleteView):
    model = Ride
    fields = '__all__'
    template_name = 'driver/confirm_ride_order_version.html'
    context_object_name = 'ride'

    def get(self, request, *args, **kwargs):
        error = []
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        driver = getDriverByRequest(request)
        toFinish = False
        return render(request, self.template_name, {'ride' : ride, 'error' : error, 'toFinish' : toFinish})

    def post(self, request, *args, **kwargs):
        error = []
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        order = Order.objects.get(ride=ride)
        driver = getDriverByRequest(request)
        toFinish = False
        if not ride.status == 'open' or driver.is_driving == True:
            # TODO: error handling, stop
            return render(request, self.template_name, {'ride' : ride, 'error' : error, 'toFinish' : toFinish})
        ride.status = 'confirmed'
        order.driver = driver
        ride.save()
        order.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return redirect(reverse('orders:ride_detail', args=[ride.id]))