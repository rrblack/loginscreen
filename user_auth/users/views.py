from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .code_generator import CodeGenerator
import random
from .forms import CustomUserCreationForm

@login_required
def login_success(request):
    messages.success(request, "You are now logged in")
    return render(request,"users/top_page.html")

User = get_user_model()


def mail_verification(request):
    generator = CodeGenerator()
    generated_code = generator.create_code()
    print(generated_code)
    if request.method == "GET":
        return render(request, "registration/mail_check.html")
    if request.method == "POST":
        code = request.POST.get("code")
        if code == "111111":
            print("code is right")
            return redirect('top_page')
        else: messages.error(request, "Invalid code")
    return redirect('mail_verification')

def mail_check(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if name and email and password:
            try:
                user = User.objects.create_user(name=name, email=email,password = password)
                print(user.__dict__)
                return redirect(reverse("mail_verification"))
            except Exception as e:
                print("Error creating user", e)
                messages.error(request, "Account already exists")
        else:
            messages.error(request, "All fields required")
    return redirect('sign_up')


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
            messages.error(request, "Email or Password Incorrect")
    return render(request, "registration/login.html")


def root_redirect(request):
    return redirect('login')

def sign_up(request):
    return render(request, "registration/sign_up.html")

def password_reset_form(request):
    return render(request,"registration/password_reset_form.html")

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = authenticate(request, email=email)
        if user is not None:
            messages.success(request, "Password reset link has been sent to your email")
            return render(request, "registration/sign_up.html")
        else:
            messages.error(request, "Email invalid")
            return render(request, "registration/login.html")

    return redirect(login)