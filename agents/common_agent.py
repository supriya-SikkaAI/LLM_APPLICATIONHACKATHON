import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = ""

def generate_openai_response(user_input,system_prompt):
    try:
        messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}]   
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"
