from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .code_generator import CodeGenerator
import random
from .forms import CustomUserCreationForm

@login_required
def login_success(request):
    messages.success(request, "You are now logged in")
    return render(request,"users/top_page.html")

User = get_user_model()


def mail_verification(request):

    if 'verification_code' not in request.session or 'pending_user' not in request.session:
        messages.error(request, "Registration session expired or invalid.")
        return redirect('sign_up')

    if request.method == "GET":
        return render(request, "registration/mail_check.html")

    if request.method == "POST":
        code = request.POST.get("code")
        stored_code = request.session['verification_code']

        if code == stored_code:
            try:
                pending_user = request.session['pending_user']
                user = User.objects.create_user(
                name=pending_user['name'],
                email=pending_user['email'],
                password=pending_user['password']
                )
                login(request, user)
                del request.session['pending_user']
                del request.session['verification_code']

                messages.success(request, "Registration successful")
                return redirect('top_page')

            except Exception as e:
                print("Error creating user", e)
                messages.error(request, "An error occurred. Please try again.")
                return redirect('mail_verification')
        else:
            messages.error(request, "Invalid code")
            return redirect('mail_verification')
    return redirect('sign_up')


def mail_check(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if name and email and password:
            try:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already registered")
                    return redirect('sign_up')
                request.session['pending_user'] = {
                    'name': name,
                    'email': email,
                    'password': password
                }
                generator = CodeGenerator()
                verification_code = generator.create_code()
                request.session['verification_code'] = verification_code
                send_mail(
                    "AUTH CODE",
                    "Here is the code: " + verification_code,
                    "from@example.com",
                    ["to@example.com"],
                    fail_silently=False,)

                print(request.session['pending_user'])
                print(request.session['verification_code'])
                return redirect(reverse("mail_verification"))
            except Exception as e:
                print("Error creating user", e)
                messages.error(request, "An error occurred. Please try again.")
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
