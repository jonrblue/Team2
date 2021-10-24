from django.shortcuts import render
from django.http import HttpResponseRedirect

# from django.contrib.auth import login, authenticate
from .forms import SignupForm

# from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect(reverse("naturescall:index"))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, "accounts/signup.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "accounts/signup.html", {"form": form})
