from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from store.models import Category


def category(request, name):
    name = name.replace('-', ' ')

    try:
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category=category)

        return render(request, 'category.html', {'products': products, 'category': category})

    except:
        return redirect('home')


def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


def product(request, pk):
    product = Product.objects.get(id=pk)

    return render(request, 'product.html', {'product': product})

def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
          
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
    
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in user:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')

    return render(request, 'register.html', {'form': form})

