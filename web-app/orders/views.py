from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Ride
from .models import RideForm
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
