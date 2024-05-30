from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import UsuarioCreationForm

class RegisterView(View):
    def get(self, request):
        form = UsuarioCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to a success page (home in this case)
        return render(request, 'registration/register.html', {'form': form})