from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomSignupForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginView(LoginView):
	template_name = "login.html"
	redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
	next_page = "/"  

def logout_view(request):
	logout(request)
	return redirect("home")

def signup_view(request):
	if request.user.is_authenticated:
		return redirect("flux")
	User = get_user_model()
	if request.method == "POST":
		form = CustomSignupForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data["username"],
				password=form.cleaned_data["password1"]
			)
			login(request, user)
			return redirect("home")  # À adapter selon ta page d'accueil
	else:
		form = CustomSignupForm()
	return render(request, "signup.html", {"form": form})

def home(request):
    form = AuthenticationForm()
    return render(request, "home.html", {"form": form})
