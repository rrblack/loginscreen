from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control

from .code_generator import CodeGenerator
import random
from .forms import CustomUserCreationForm

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
        print("Code that got carried over is", stored_code)

        if code == stored_code:
            try:
                pending_user = request.session['pending_user']
                print("The user that got carried over is", pending_user)
                user = User.objects.create_user(
                name=pending_user['name'],
                email=pending_user['email'],
                password=pending_user['password']
                )
                del request.session['pending_user']
                del request.session['verification_code']
                login(request, user)
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
                    "メールアドレス認証コードはこちらです: " + verification_code,
                    "mail@kanri.com",
                    [email],
                    fail_silently=False,)

                print("Before redirect:", request.session.get('verification_code'))
                print("Before redirect:", request.session.get('pending_user'))
                print("Session data before redirect:", request.session.items())
                request.session.save()
                return redirect(reverse("mail_verification"))
            except Exception as e:
                print("Error making user", e)
                messages.error(request, "An error occurred. Please try again.")
        else:
            messages.error(request, "All fields required")
    return redirect('sign_up')
def custom_logout(request):
    logout(request)
    request.session.delete()
    messages.success(request, "You are now logged out.")
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
            messages.error(request, "Email or Password Incorrect")
    return render(request, "registration/login.html")


def root_redirect(request):
    return redirect('login')

def sign_up(request):
    return render(request, "registration/sign_up.html")
