import openai
from dotenv import load_dotenv
import os
from sikka_request_key import get_sikka_request_key
from sikka_api_csv import sikka_api_csv
from json_helpers import extract_json

# Load environment variables
load_dotenv()
openai.api_key = ""

# Define available actions for reputation management system
available_actions = {
    'get_sikka_request_key': get_sikka_request_key,
    'sikka_api_csv': sikka_api_csv
}

def generate_payment_response(user_question, system_prompt):
    """Generate a response using the reputation management agent logic."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]

    def generate_text_with_conversation():
        """Creates the chat completion using OpenAI."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0
        )
        return response.choices[0].message.content

    turn_count = 1
    max_turns = 5
    answer = None

    while turn_count < max_turns:
        print(f"Loop: {turn_count}")
        turn_count += 1
        response = generate_text_with_conversation()
        print(response)

        # Extract and handle JSON
        json_function = extract_json(response)

        if json_function:
            function_name = json_function[0]['function_name']
            function_params = json_function[0]['function_params']

            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}")

            print(f" -- running {function_name} with {function_params}")
            action_function = available_actions[function_name]

            # Execute the action
            result = action_function(**function_params)
            function_result_message = f"Action_Response: {result}"

            # Add the result to the conversation
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
        else:
            answer = response
            break

    return answer
