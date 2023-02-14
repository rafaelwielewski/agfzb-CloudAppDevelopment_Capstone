from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from djangoapp.models import CarModel, CarMake
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def simple(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/simpleTemplate.html', context)

# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://e4db4b20.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealeship_list = get_dealers_from_cf(url)
        context["dealership_list"] = dealeship_list
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://e4db4b20.eu-gb.apigw.appdomain.cloud/api/review"
        context["reviews_list"] = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context["dealer_id"] = dealer_id
        #reviews_names = ' '.join([review.name+": "+review.review+"("+review.sentiment+")" for review in reviews])
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    print(request.user.is_authenticated)
    if(request.user.is_authenticated):
        if request.method == "POST":
            review = dict()
            car = CarModel.objects.get(id=request.POST['car'])
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            review["car_make"] = car.carMake.name
            
            review["name"] = request.user.username
            review["review"] = request.POST['content']
            review["purchase"] = request.POST['purchase']
            review["dealership"] = dealer_id
            review["purchase_date"] = request.POST['purchase_date']

            json_payload = dict()
            json_payload["review"] = review

            url = "https://e4db4b20.eu-gb.apigw.appdomain.cloud/api/review"
            result = post_request(url, json_payload=json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        elif request.method == "GET":
            context["cars"] = CarModel.objects.filter(dealerId=dealer_id)
            return render(request, "djangoapp/add_review.html", context)
    else:
        return render(request, 'djangoapp/login.html', context)
