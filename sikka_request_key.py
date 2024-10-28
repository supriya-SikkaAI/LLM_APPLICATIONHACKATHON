import requests
import json

def get_sikka_request_key(url, office_id, secret_key, app_id, app_key):
    body = {
        "grant_type": "request_key",
        "office_id": office_id,
        "secret_key": secret_key,
        "app_id": app_id,
        "app_key": app_key
    }
    
    # Make the request to the Sikka API
    RequestKey_response = requests.post(url, json=body)
    
    # Check for response success
    if RequestKey_response.status_code != 200:
        return {"error": "Failed to obtain request key", "details": RequestKey_response.text}
    
    json_format = RequestKey_response.json()
    request_key = json_format.get('request_key')
    
    if not request_key:
        return {"error": "No request key returned", "details": json_format}
    
    Api_url = "https://api.sikkasoft.com/v4/patients"
    headers1 = {'Request-Key': request_key}
    Api_response = requests.get(Api_url, headers=headers1)
    
    return Api_response.json()  # Ensure the response is returned in JSON format
