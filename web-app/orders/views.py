from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import authenticate, UserCreationForm
from django.shortcuts import render, redirect


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
