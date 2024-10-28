import pandas as pd
import requests
import spacy  # You can install via 'pip install spacy'

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load the spreadsheet containing table names and base URLs
df = pd.read_excel("API_Sikka.csv")  # Replace with your file path
url_mapping = df.set_index('Table/Key Name').to_dict('index')

# Define keyword-intent mappings (for custom logic)
intent_to_table_key = {
    "reputation management": "patients",
    "payment": "transactions",
    "billing or payments": "transactions",
    "communication": "patients"
}

def map_intent_to_table_key(prompt):
    # Use NLP to extract keywords and intent
    doc = nlp(prompt.lower())
    prompt_keywords = [token.text for token in doc]

    # Try to match the prompt to a known intent-to-table mapping
    for intent, table_key in intent_to_table_key.items():
        if intent in prompt:
            return table_key

    # If no specific intent is detected, check for any known table name in the prompt
    for table_key in url_mapping.keys():
        if table_key in prompt_keywords:
            return table_key

    return None  # If no match found, return None

def get_sikka_data(table_key, office_id, secret_key, app_id, app_key):
    if table_key not in url_mapping:
        return {"error": f"Table/Key '{table_key}' not found"}

    # Construct the full API URL
    base_url = url_mapping[table_key]['Base URL']
    api_url = f"{base_url}{table_key}"

    # Request body to get the request key
    request_body = {
        "grant_type": "request_key",
        "office_id": office_id,
        "secret_key": secret_key,
        "app_id": app_id,
        "app_key": app_key
    }

    # Make the request to get the request key
    request_key_response = requests.post(base_url, json=request_body)
    if request_key_response.status_code != 200:
        return {"error": "Failed to obtain request key", "details": request_key_response.text}

    # Extract the request key from the response
    request_key = request_key_response.json().get('request_key')
    if not request_key:
        return {"error": "No request key returned", "details": request_key_response.json()}

    # Use the request key to call the API
    headers = {'Request-Key': request_key}
    api_response = requests.get(api_url, headers=headers)

    if api_response.status_code != 200:
        return {"error": "API call failed", "details": api_response.text}

    return api_response.json()

def handle_user_prompt(prompt, office_id, secret_key, app_id, app_key):
    # Map the user’s intent to the correct table key
    table_key = map_intent_to_table_key(prompt)
    
    if not table_key:
        return {"error": "Could not determine the appropriate API to call from the prompt"}

    # Fetch the data from the appropriate API
    response = get_sikka_data(table_key, office_id, secret_key, app_id, app_key)
    return response
