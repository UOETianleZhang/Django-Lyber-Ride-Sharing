from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import Http404
from .models import Choice, Question, Ride, Order, RiderSharer
from .models import  RiderDriver
from .forms import RideForm, RiderDriverForm, ShareSearchForm, OrderForm
import datetime


from django.contrib.auth.mixins import LoginRequiredMixin


def home_view(request, *args, **kwargs):
    if request.method == 'POST':
        if 'rider' in request.POST:
            return HttpResponseRedirect('orders/menu_rider/')
        elif 'driver' in request.POST:
            if not RiderDriver.objects.filter(user=request.user).exists():
                return HttpResponseRedirect('driver/newDriver')
            else:
                return HttpResponseRedirect('orders/menu_driver/')

    return render(request, "home.html", {})


@login_required()
def user_page_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    # request, template name, context info
    return render(request, "userPage.html", {})


def create_driver_view(request):
    form = RiderDriverForm()
    errors = []
    if request.method == 'POST':
        form = RiderDriverForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.pk)
            # user = User.objects.get(username__exact=request.user)
            driver = RiderDriver(user=user,plateNumber=form.cleaned_data['plate_number'],
                              vehicle_type=form.cleaned_data['vehicle_type'],
                              max_passenger_num=form.cleaned_data['max_passenger_num'],
                              special_info=form.cleaned_data['special_info'],
                                 driverName=form.cleaned_data['driver_name'],
                                 is_driving=False)
            driver.save()
            return HttpResponseRedirect('/')
        else:
            errors.append("not valid")
    return render(request, "driver/new_driver.html", {'form' : form, 'errors' : errors})


# Create your views here.
def signup_view(request, *args, **kwargs):
    errors = []
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request, user)
            return redirect('/accounts/login')
        errors.append("not valid")
    else:
        errors.append("not valid")
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'user': form, 'errors': errors})


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/index.html'


class RequestRideView(LoginRequiredMixin, generic.CreateView):
    form_class = RideForm
    template_name = 'orders/request_ride.html'
    context_object_name = 'latest_question_list'

    def form_valid(self, form):
        ride = form.save(commit=False)
        ride.status = 'open'
        ride.total_cur_passenger_num = ride.owner_passenger_num
        ride = form.save()
        Order.objects.create(owner=self.request.user, ride=ride, can_share=ride.can_share, total_cur_passenger_num=ride.total_cur_passenger_num)
        return redirect('orders:check_ride_rider')

    def get_success_url(self):
        return reverse('orders:check_ride_rider')


class MenuViewRider(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/menu_rider.html'


class CheckRideViewRider(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/check_ride_rider.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'rider'
        return context

    def get_queryset(self):
        return Ride.objects.filter(order__owner_id__exact=self.request.user.id)\
            .exclude(status__in=['completed', 'confirmed'])


class MenuViewDriver(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/menu_driver.html'

    def post(self, request, *args, **kwargs):
        if 'open_orders' in request.POST:
            return HttpResponseRedirect('../check_order_driver/')
        elif 'current_orders' in request.POST:
            return HttpResponseRedirect('../check_my_ride_driver/')
        return render(request, template_name=self.template_name)


class CheckRideViewDriver(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/check_ride_driver.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        return Ride.objects.filter(status__exact='open')


# class CheckMyRideViewDriver(LoginRequiredMixin, generic.ListView):
#     template_name = 'orders/check_my_ride_driver.html'
#     context_object_name = 'latest_ride_list'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['role'] = 'driver'
#         return context
#
#     def get_queryset(self):
#         return Ride.objects.filter(status__exact='open')


class ModifyRideView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/modify_ride.html'
    model = Ride
    fields = ['starting_point', 'destination', 'start_time', 'vehicle_type', 'special_request', 'owner_passenger_num', 'can_share']
    context_object_name = 'ride'

    def form_valid(self, form):
        prev_owner_passenger_num = self.object.owner_passenger_num
        ride = form.save(commit=False)
        ride.total_cur_passenger_num = ride.total_cur_passenger_num - prev_owner_passenger_num + ride.owner_passenger_num
        ride = form.save()
        order = Order.objects.filter(ride_id__exact=ride.id)[0]
        order.total_cur_passenger_num = ride.total_cur_passenger_num
        order.can_share = ride.can_share
        order.save()
        return redirect('orders:check_ride_rider')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['owner_name'] = self.request.user.username
        return context

    # cannot modify a ride that already has
    def get_queryset(self):
        return Ride.objects\
            .filter(order__owner_id__exact=self.request.user.id, order__ridersharer__isnull=True)\
            .exclude(status__exact='completed')

    def get_success_url(self):
        return reverse('orders:check_ride_rider')

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect("orders:modify_fail")
        return super().get(request, *args, **kwargs)


class ModifyFailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/modify_failed.html'


class JoinRideSearchView(LoginRequiredMixin, generic.FormView):
    form_class = ShareSearchForm
    template_name = 'orders/join_ride_search.html'


class JoinRideListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/join_ride_list.html'
    context_object_name = 'ride_list'

    def get_queryset(self):
        num_passengers = self.request.GET.get("num_passengers")
        special_request = int(self.request.GET.get("special_request"))
        destination = self.request.GET.get("destination")
        start_time = self.request.GET.get("start_time")
        messages.info(self.request, str(num_passengers))
        if num_passengers and destination and start_time:
            result = Ride.objects.filter(
                                            max_passenger_num__gte=F('total_cur_passenger_num') + num_passengers,
                                            special_request__exact=special_request,
                                            destination__exact=destination,
                                            can_share__exact=True,
                                            start_time__gt=(datetime.datetime.strptime(start_time,'%Y-%m-%dT%M:%S') - datetime.timedelta(minutes=30)),
                                            # start_time__range=(
                                            # datetime.datetime.strptime(start_time, '%Y-%m-%dT%M:%S')-datetime.timedelta(minutes=30),
                                            # datetime.datetime.strptime(start_time, '%Y-%m-%dT%M:%S')+datetime.timedelta(minutes=30))
                                         )\
                                    .exclude(order__owner_id__exact=self.request.user.id)\
                                    .exclude(order__ridersharer__user=self.request.user)
        else:
            result = None
        return result


class JoinRideView(LoginRequiredMixin, generic.DetailView):
    template_name = 'orders/join_ride_detail.html'
    model = Ride
    context_object_name = 'ride'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = Order.objects.filter(ride_id__exact=self.object.id)[0]
        context['sharer'] = order.ridersharer_set.all()
        context['owner_name'] = order.owner.username
        return context

    def post(self, request, *args, **kwargs):
        try:
            ride = get_object_or_404(Ride, pk=kwargs['pk'])
        except Http404:
            return redirect(reverse("orders:join_fail"))
        order = Order.objects.filter(ride__exact=ride)[0]
        sharer_passenger_num = int(messages.get_messages(self.request)._loaded_messages[-1].message)
        ridesharer = RiderSharer(user=request.user, sharer_passenger_num=sharer_passenger_num)
        ridesharer.save()
        ridesharer.order.add(order)
        order.ridersharer_set.add(ridesharer)
        order.total_cur_passenger_num += sharer_passenger_num
        ride.total_cur_passenger_num += sharer_passenger_num
        order.save()
        ride.save()
        messages.get_messages(self.request).used = True
        return redirect(reverse('orders:ride_detail', args=[ride.id]))

    def get_queryset(self):
        return Ride.objects.exclude(order__ridersharer__user__in=[self.request.user])

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect("orders:join_fail")
        return super().get(request, *args, **kwargs)


class JoinRideFailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/join_ride_failed.html'


def confirm(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.status = 'completed'
    ride.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('orders:ride_detail', args=(ride.id)))


class RideDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ride
    template_name = 'orders/ride_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = Order.objects.filter(ride_id__exact=self.object.id)[0]
        context['sharer'] = order.ridersharer_set.all()
        context['owner_name'] = order.owner.username
        context['driver'] = order.driver
        context['ride'] = order.ride
        return context

    def get_queryset(self):
        return Ride.objects.exclude(status__exact="completed")

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect("orders:join_fail")
        return super().get(request, *args, **kwargs)


class MyRideView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/my_ride_list.html'
    context_object_name = 'my_ride_list'

    def get_queryset(self):
        return Ride.objects.filter(Q(order__owner_id__exact=self.request.user.id)| Q(order__ridersharer__user_id=self.request.user.id)).exclude(status__exact="completed")

