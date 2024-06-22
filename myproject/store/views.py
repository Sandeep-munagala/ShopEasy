from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products' : products})

def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,("you have been logged in"))
            return redirect('home')
        else:
            messages.success(request,("you have entered wrong username/password"))
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out !"))
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created Successfully..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})
      

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product' : product})

def category(request, foo):
	foo = foo.replace('-', ' ')
	try:
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(Category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')
      
def add_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    try:
        cart_item = Cart.objects.get(product_id=product)
        cart_item.quantity += 1
        cart_item.save() 
    except Cart.DoesNotExist:
        Cart.objects.create(product_id=product)
    return redirect('cart_view')


def cart_view(request):
    cart_items = Cart.objects.all()
    # sorted_cart_items = sorted(cart_items, key=lambda x: not x.product.is_sale)
    products = [{'product': item.product_id, 'quantity': item.quantity} for item in cart_items]
    return render(request, 'cart_view.html', {'products': products})


def delete_item(request, pk):
    cart_item = get_object_or_404(Cart, product_id=pk)
    
    if cart_item.quantity == 1:
        cart_item.delete()
        messages.success(request, "Item removed from the cart.")
    else: 
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, "Quantity updated.")

    return redirect('cart_view')
