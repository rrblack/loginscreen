from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

@login_required
def login_success(request):
    return render(request,"users/top_page.html")

User = get_user_model()

def mail_check(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if name and email and password:
            user = User.objects.create_user(name=name, email=email,password = password)
            print(user.__dict__)
            print(user.save())
            return redirect('login')


def users_login(request):
    if request.method == "POST":
        print(request)
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(f"Received Email: {email}, Received Password: {password}")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            return redirect("top_page")
        else:
            return render(request, "registration/sign_up.html")
    return render(request, "registration/login.html")


def root_redirect(request):
    return redirect('login')

def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("mail_check"))
        else:
            print(form.errors)

    else:
        form = CustomUserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})