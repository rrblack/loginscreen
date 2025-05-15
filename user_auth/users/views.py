from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

from .forms import CustomUserCreationForm

def top_page(request):
    return render(request, "users/top_page.html")

def mail_check(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
    return render(request, "registration/mail_check.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            return redirect("top_page")
        else:
            messages.error(request, "Invalid email")
            return redirect(request,"login.html")
    return render(request, "login.html")



def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect(reverse("mail_check"))
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})