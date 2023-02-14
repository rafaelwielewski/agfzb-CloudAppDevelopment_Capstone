import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key:
            print(api_key)
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, params={})
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, params={"state":state})
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealership"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, params={"dealerId":dealer_id})
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment="neutral",
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    result = "neutral"
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/e014f0e6-770a-45ef-b5f7-462533c20561/v1/analyze?version=2022-04-07"
    api_key = "0LFYJYpCixtbGj61nbRQi-_qxajeW8rWkyQHQX0NqtHP"
    params = dict()
    params["text"] = dealerreview
    params["features"] = "keywords"
    params["entities.emotion"] = "false"
    params["entities.sentiment"] = "false"
    params["keywords.emotion"] = "false"
    params["keywords.sentiment"] = "true"
    json_result = get_request(url, params=params, api_key=api_key)
    if json_result:
        print(json_result)
        if "keywords" in json_result:
            print("entra")
            keywords = json_result["keywords"]
            result = keywords[0]["sentiment"]["label"]
            #print(result)
    return result