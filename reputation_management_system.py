import requests

def get_google_reviews(place_id,api_key):
    #place_id="ChIJxUegZSjPj4ARuzlsorzuj1A"
    #api_key = "api_key"
    # URL to fetch place details, including reviews
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        place_details = response.json()

        # Check if the place details include reviews
        if 'result' in place_details and 'reviews' in place_details['result']:
            reviews = place_details['result']['reviews']
            return reviews
        else:
            return "No reviews found for this place."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_facebook_reviews(page_id, access_token):
    page_id=""
    access_token=""
    url = f"https://graph.facebook.com/v12.0/{page_id}/ratings?access_token={access_token}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        reviews = response.json()
        
        if 'data' in reviews:
            return reviews['data']
        else:
            return "No reviews found for this page."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
import requests

def get_yelp_reviews(business_id,api_key):
    #business_id="OPN5iwWHgIo8xHl4YdwMUg"
    #api_key="yN1kvJoqChceNK_yd4yd5XQ369g0dEyYteVincs8_jfWoBcNLrtnop3TEAPki6Kxt-k3Q1I5vtA8Dw9F7meuNsqjxq7RTAu5TItLBgU3iPVw05QI7NRHJbZZo1wZZ3Yx"
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        reviews = response.json()
        
        if 'reviews' in reviews:
            return reviews['reviews']
        else:
            return "No reviews found for this business."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


