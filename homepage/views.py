from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from customers import views
from .forms import UserCreateForm
from customers.models import *
# from customers.forms import  CustomerForm
from customers.models import order




def index(request):
    page = 'login'

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            print("Username does not exist")
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('loggedin')
        else:
            print("Username or password is incorrect")

    context = {'page':page}
    return render(request, "homepage/index.html",context)

@login_required(login_url='login')
def loggedIn(request):
    payment_successful = request.GET.get('payment_successful', 'False') == 'True'
    
    context = {
        'payment_successful': payment_successful
    }
    
    return render(request,"homepage/loggedin.html",context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

# user = Customer.objects.get(id =pk)
# print(user)

# def feedback(request):
    
#     user = request.user.id
#     required_user = Customer.objects.get(id = user)
#     print(required_user)
#     # form = CustomerFeedbackForm(instance=required_user)
#     # if request.method == 'POST':
#     #     form = CustomerFeedbackForm(request.POST, instance=required_user)
#     #     if form.is_valid():
#     #         form.save()
#     #         messages.success(request, "Your feedback sent successfully. Thank you.")
#     # context = {'form':form}
#     return render(request,"homepage/feedback.html")

# def registerUser(request):
#     page = 'register'
#     form = UserCreateForm()

#     if request.method=="POST":
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
           
#             user.save()
#             messages.success(request, 'User account created successfully')

#     context={'page':page, 'form':form}
#     return render(request, 'homepage/index.html',context)







def registerUser(request):
    page = 'register'
    
    # Handle GET and POST requests differently
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Display success message
            messages.success(request, 'User account created successfully')

            # Redirect after successful registration to avoid resubmission on page refresh
            return redirect('login')  # Replace 'login' with your actual redirect target
        else:
            # Form is invalid, let Django handle error messages automatically
            messages.error(request, 'Please correct the errors below.')

    else:
        # For GET requests, initialize the form with no data
        form = UserCreateForm()

    context = {'page': page, 'form': form}
    return render(request, 'homepage/index.html', context)

    
    
def view_cart(request):
    # user = User.objects.filter(username="himanshu").first()
    user = request.user

    
    user_order = order.objects.filter(user=user).last()
    
    print(user_order)
    
    if not user_order:
        return render(request, 'cart/selected_plan.html', {'error': "No payment found."})
    
    

    return render(request, 'cart/selected_plan.html', {'order': user_order})
