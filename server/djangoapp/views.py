# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate

from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request (API endpoint)
@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": "error",
            "error": "Method not allowed. Use POST."
        }, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                "status": "error",
                "error": "Username and password are required"
            }, status=400)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
        else:
            return JsonResponse({
                "userName": username,
                "status": "Failed",
                "error": "Invalid credentials"
            }, status=401)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "status": "error",
            "error": "Invalid JSON"
        }, status=400)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "error": "An error occurred during login"
        }, status=500)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """
    Logout the current user and redirect to home page
    """
    logger.info(f"Logout request received. User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    logout(request)
    logger.info("User logged out successfully")
    return JsonResponse({"userName": "", "status": "Logged out"})


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    """
    Handle user registration
    """
    if request.method != 'POST':
        return JsonResponse({
            "status": "error",
            "error": "Method not allowed. Use POST."
        }, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        
        if not username or not password:
            return JsonResponse({
                "status": "error",
                "error": "Username and password are required"
            }, status=400)
        
        username_exist = False
        email_exist = False
        
        try:
            User.objects.get(username=username)
            username_exist = True
        except User.DoesNotExist:
            logger.debug("{} is new user".format(username))
        
        if email:
            try:
                User.objects.get(email=email)
                email_exist = True
            except User.DoesNotExist:
                logger.debug("Email {} is available".format(email))
        
        if not username_exist:
            if not email_exist:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email
                )
                login(request, user)
                data = {
                    "userName": username,
                    "status": "Authenticated"
                }
                return JsonResponse(data)
            else:
                data = {
                    "userName": username,
                    "error": "Email already registered"
                }
                return JsonResponse(data, status=400)
        else:
            data = {
                "userName": username,
                "error": "Already Registered"
            }
            return JsonResponse(data, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "status": "error",
            "error": "Invalid JSON"
        }, status=400)
    except KeyError as e:
        return JsonResponse({
            "status": "error",
            "error": f"Missing required field: {str(e)}"
        }, status=400)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "error": "An error occurred during registration"
        }, status=500)


# Get current logged in user
def get_current_user(request):
    """
    Get the current logged in user
    """
    if request.user.is_authenticated:
        return JsonResponse({
            "userName": request.user.username,
            "status": "Authenticated"
        })
    else:
        return JsonResponse({
            "userName": None,
            "status": "Not authenticated"
        }, status=401)


# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state=None):
    """
    Get all dealerships or filter by state
    """
    try:
        if state:
            url = f"https://francesco123-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/fetchDealers/{state}"
        else:
            url = "https://francesco123-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/fetchDealers"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dealers = response.json()
            return JsonResponse({"status": "success", "dealers": dealers})
        else:
            return JsonResponse({
                "status": "error",
                "message": f"API returned status {response.status_code}"
            }, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error connecting to API: {str(e)}"
        }, status=500)


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    """
    Get reviews for a specific dealer
    """
    try:
        url = f"https://francesco123-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/fetchReviews/dealer/{dealer_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            reviews = response.json()
            return JsonResponse({"status": "success", "reviews": reviews})
        else:
            return JsonResponse({
                "status": "error",
                "message": f"No reviews found"
            }, status=404)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    """
    Get details for a specific dealer
    """
    try:
        url = f"https://francesco123-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/fetchDealer/{dealer_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dealer = response.json()
            return JsonResponse({"status": "success", "dealer": dealer})
        else:
            return JsonResponse({
                "status": "error",
                "message": f"Dealer not found"
            }, status=404)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)


# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    """
    Add a review for a dealer with sentiment analysis
    """
    if request.method != 'POST':
        return JsonResponse({
            "status": 405,
            "message": "Method not allowed. Use POST."
        }, status=405)
    
    if request.user.is_anonymous:
        return JsonResponse({
            "status": 403,
            "message": "Unauthorized. Please login."
        }, status=403)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "status": 400,
                    "message": f"Missing required field: {field}"
                }, status=400)
        
        # ✅ Sentiment analysis via external API (single attempt, 60s timeout)
        import urllib.parse
        
        review_text = data['review']
        sentiment = 'neutral'  # Default fallback
        
        try:
            review_text_encoded = urllib.parse.quote(review_text)
            sentiment_url = f"https://sentianalyzer.22m7z7gwa2om.us-south.codeengine.appdomain.cloud/analyze/{review_text_encoded}"
            
            logger.info(f"📞 Calling sentiment API for: '{review_text[:50]}...'")
            
            sentiment_response = requests.get(
                sentiment_url, 
                timeout=60,  # 60 seconds for cold start
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if sentiment_response.status_code == 200:
                sentiment_data = sentiment_response.json()
                sentiment = sentiment_data.get('sentiment', 'neutral')
                logger.info(f"✅ Sentiment from API: {sentiment}")
            else:
                logger.warning(f"⚠️ API returned status {sentiment_response.status_code}, using neutral")
                
        except requests.exceptions.Timeout:
            logger.error("⏱️ Sentiment API timeout (60s exceeded), using neutral")
            
        except Exception as e:
            logger.error(f"❌ Sentiment API error: {str(e)}, using neutral")
        
        # Add sentiment to review data
        data['sentiment'] = sentiment
        
        # Save review to MongoDB via Node.js API
        mongodb_url = "https://francesco123-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/insert_review"
        
        response = requests.post(
            mongodb_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        logger.info(f"📝 Review submission response: {response.status_code}")
        
        if response.status_code == 200:
            review_data = response.json()
            logger.info(f"✅ Review saved successfully with sentiment: {sentiment}")
            return JsonResponse({
                "status": 200,
                "message": "Review added successfully",
                "review": review_data,
                "sentiment": sentiment
            })
        else:
            logger.error(f"❌ Error from MongoDB API: {response.text}")
            return JsonResponse({
                "status": response.status_code,
                "message": "Error saving review to database"
            }, status=response.status_code)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "status": 400,
            "message": "Invalid JSON"
        }, status=400)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to API: {str(e)}")
        return JsonResponse({
            "status": 500,
            "message": f"Error connecting to database: {str(e)}"
        }, status=500)
    except Exception as e:
        logger.error(f"Unexpected error in add_review: {str(e)}")
        return JsonResponse({
            "status": 500,
            "message": f"Error: {str(e)}"
        }, status=500)


# Get cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


# View to populate database
def populate_database(request):
    """
    Populate database with initial CarMake and CarModel data
    """
    try:
        CarMake.objects.all().delete()
        CarModel.objects.all().delete()
        
        initiate()
        
        return JsonResponse({
            "status": "success",
            "message": "Database populated successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
