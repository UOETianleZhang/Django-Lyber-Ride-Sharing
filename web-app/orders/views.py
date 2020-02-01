from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Ride
from .models import RideForm

def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    # request, template name, context info
    return render(request, "home.html", {})


@login_required()
def user_page_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    # request, template name, context info
    return render(request, "userPage.html", {})

@login_required()
def driver_page_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    # request, template name, context info
    return render(request, "driverPage.html", {})


# Create your views here.
def signup_view(request, *args, **kwargs):
    errors = []
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/accounts/login')
        errors.append("not valid")
    else:
        errors.append("not valid")
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'user': form, 'errors': errors})

class IndexView(generic.ListView):
    template_name = 'orders/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class RequestRideView(generic.CreateView):
    # model = Ride
    form_class = RideForm
    # print(form_class)
    # fields = '__all__'
    template_name = 'orders/request_ride.html'
    context_object_name = 'latest_question_list'
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects

    def get_success_url(self):
        return reverse('orders:check_ride')


class CheckRideView(generic.ListView):
    template_name = 'orders/check_ride.html'
    context_object_name = 'latest_ride_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['role'] = 'rider_owner'
        print(context)
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Ride.objects.order_by('start_time')[:5]


class ModifyRideView(generic.UpdateView):
    template_name = 'orders/modify_ride.html'
    model = Ride
    fields = '__all__'
    context_object_name = 'ride'
    def get_success_url(self):
        return reverse('orders:check_ride')


class ConfirmRideView(generic.DetailView):
    model = Ride
    template_name = 'orders/confirm_ride.html'

def confirm(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.status = 'confirmed'
    ride.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('orders:ride_detail', args=(ride.id)))

class RideDetailView(generic.DetailView):
    model = Ride
    template_name = 'orders/ride_detail.html'

class DetailView(generic.DetailView):
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
