from flask import Flask, render_template, request, jsonify
#from prompts import system_prompt
#from agents.rpm_test import rpm_prompt
from agents.rpm_prompts import rpm_prompt
from agents.rpm_agent import generate_reputation_management_response
from agents.payments_agent import generate_payment_response
from agents.payments_prompts import payments_prompt
from agents.business_performance_management_agent import generate_business_performance_management_response
from agents.business_performance_management_prompt import business_performance_management_prompt
from agents.paient_communication_system_agent import generate_patient_communication_system_response
from agents.paient_communication_system_prompts import patient_communication_system_prompt
from agents.common_agent import generate_openai_response
from agents.common_prompt import common_system_prompt
app = Flask(__name__)

def determine_agent_from_input(user_input):
    """Determine which agent to call based on the user's input."""
    user_input = user_input.lower()

    # Simple keyword matching to route to the appropriate agent
    if any(keyword in user_input.lower() for keyword in ["reputation", "repu", "repo", "reviews", "feedback","reputacion", "repotation", "reputition","reputatoin", "reputasion", "repoutation", "repputation"]):
        return 'reputation_management'
    elif any(keyword in user_input.lower() for keyword in ["payment", "payments", "pay", "transaction", "payments system","pament", "pymant", "paymant", "paymet", "transction", "tranaction", "trasaction","billing", "invoice", "checkout", "gateway"]):
        return 'payment'
    elif any(keyword in user_input.lower() for keyword in ["communication", "comm", "chat", "messages", "patient communication system","comunication", "comms", "msg","messaging", "text", "sms", "email", "call", "notification"]):
        return 'communication'
    elif any(keyword in user_input.lower() for keyword in ["business", "bussiness", "bus", "performance", "management","business performance management system", "performence", "managment", "perf", "kpi", "metrics", "analytics", "reporting", "strategy", "goals"]):
        return 'business'
    elif any(keyword in user_input.lower() for keyword in ["improve", "code", "generate", "more", "detailed","steps"]):
        return 'follow_up'
    else:
        return None

@app.route('/')
def home():
    return render_template('index_latest.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Get the user's question from the request
        user_question = request.json['question']

        # Determine the appropriate agent based on the user's input
        agent = determine_agent_from_input(user_question)
        if agent == 'reputation_management':
            # Call the reputation management agent
            answer = generate_reputation_management_response(user_question, rpm_prompt)
        elif agent == 'payment':
            # Call the reputation management agent
            answer = generate_payment_response(user_question, payments_prompt)
        elif agent == 'business':
            # Call the reputation management agent
            answer = generate_business_performance_management_response(user_question, business_performance_management_prompt)
        elif agent == 'communication':
            # Call the reputation management agent
            answer = generate_patient_communication_system_response(user_question, patient_communication_system_prompt)
        elif agent == 'follow_up':
            answer = generate_openai_response(user_question,common_system_prompt)
        else:
            answer = "I'm sorry, I couldn't identify the system you're referring to.Please try again with one of the following areas: Reputation Management, Payment, Communication, or Business Performance.For example, you could ask 'help me build payments system'"

        # Return the answer in JSON response
        return jsonify({
            'status': 'success',
            'answer': answer
        })

    except openai.error.OpenAIError as e:
        return jsonify({
            'status': 'error',
            'message': f'OpenAI API Error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
