from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # also fixed missing POST data
        if form.is_valid():
            form.save()
            return redirect('login')  # Optional: redirect to login after register
        return render(request, 'accounts/register.html', {"form": form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {"form": form})
