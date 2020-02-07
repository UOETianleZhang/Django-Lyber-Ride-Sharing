from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .driver_view import getDriverByRequest
from .models import Choice, Question, Ride, Order
from .models import RideForm, RiderDriver, ShareSearchForm
from .forms import RiderDriverForm
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


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class RequestRideView(LoginRequiredMixin, generic.CreateView):
    # model = Ride
    form_class = RideForm
    # print(form_class)
    # fields = '__all__'
    template_name = 'orders/request_ride.html'
    context_object_name = 'latest_question_list'

    def form_valid(self, form):
        ride_form = form.save(commit=False)
        ride_form.status = 'open'
        ride = form.save()
        Order.objects.create(owner=self.request.user, ride=ride)
        return redirect('orders:check_ride_rider')

    def get_success_url(self):
        return reverse('orders:check_ride_rider')


class MenuViewRider(LoginRequiredMixin, generic.TemplateView):
    template_name = 'orders/menu_rider.html'





class CheckRideViewRider(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/check_ride_rider.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'rider'
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Ride.objects.filter(order__owner_id__exact=self.request.user.id)\
            .exclude(status__exact='confirmed')

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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Ride.objects.filter(status__exact='open')

class CheckMyRideViewDriver(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/check_my_ride_driver.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'driver'
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Ride.objects.filter(status__exact='open')

class ModifyRideView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/modify_ride.html'
    model = Ride
    fields = ['starting_point', 'destination', 'start_time', 'vehicle_type', 'special_request', 'max_passenger_num', 'cur_passenger_num']
    context_object_name = 'ride'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['owner_name'] = self.request.user.username
        return context

    # cannot modify a ride that already has
    def get_queryset(self):
        return Ride.objects.filter(order__owner_id__exact=self.request.user.id, order__ridersharer__isnull=True)

    def get_success_url(self):
        return reverse('orders:check_ride_rider')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If pk not defined, it's an error.
        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == None:
            return redirect("orders:modify_fail")
        else:
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
        if num_passengers and destination and start_time:
            result = Ride.objects.filter(
                                            max_passenger_num__gte=F('cur_passenger_num') + num_passengers,
                                             special_request__exact=special_request,
                                             destination__exact=destination,
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

    def post(self, request, *args, **kwargs):
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        ride.save()
        order = Order.objects.filter(ride__exact=ride)[0]
        order.ridersharer_set.create(user=request.user, order=order)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return redirect(reverse('orders:ride_detail', args=[ride.id]))


def confirm(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.status = 'confirmed'
    ride.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('orders:ride_detail', args=(ride.id)))


class RideDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ride
    template_name = 'orders/ride_detail.html'


class MyRideView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/my_ride_list.html'
    context_object_name = 'my_ride_list'

    def get_queryset(self):
        return Ride.objects.filter(Q(order__owner_id__exact=self.request.user.id)| Q(order__ridersharer__user_id=self.request.user.id))


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'orders/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'orders/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'orders/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('orders:results', args=(question.id)))
