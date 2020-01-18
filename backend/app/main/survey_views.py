from flask import url_for, session, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from . import main
from .models import Survey

# Main control flow: direct user to welcome message or next question
@main.route('/message', methods=['GET'])
def sms_signup():
    response = MessagingResponse()

    signup_survey = Survey.query.first()
    if survey_error(signup_survey, response.message):
        return str(response)
    
    session['id'] = request.values['From']
    
    if 'question_id' in session:
        # Retrieve the client's phone number and format it
        phone_number = "%2B" + request.values.get('From', None)[1: ]
        # Retrieve the record id to check if the client registered before
        response_id = retrieve_prev_record(phone_number)
        # Redirect the response to the answer-saving url
        answer_url = url_for('main.answer', question_id=session['question_id'], record_id=response_id)
        response.redirect(url=answer_url)
    elif request.values.get('Body', None).strip() == 'SIGNUP':
        redirect_to_first_question(response, signup_survey)
    elif request.values.get('Body', None).strip() == 'MOVEUP':
        welcome_user(signup_survey, response.message)
    else:
        response.message(None)
    return str(response)


# Catch survey errors
def survey_error(survey, send_function):
    if not survey:
        send_function('No survey exists')  # we need to dbseed
        return True
    elif not survey.has_questions:
        send_function('No questions')
        return True
    return False


# Route the user to the first question
def redirect_to_first_question(response, survey):
    first_question = survey.questions.order_by('id').first()
    first_question_url = url_for('main.question', question_id=first_question.id)
    response.redirect(url=first_question_url, method='GET')


# Send a welcome message to the user
def welcome_user(survey, send_function):
    welcome_text = 'Welcome to Move Up! To sign up and get paired with a mentor, you can either continue here or head to our online form (https://bit.ly/moveup-signup). To continue here, please respond SIGNUP.'
    send_function(welcome_text)

# Check if record already exists
def retrieve_prev_record(phone_number):
    prev_response = requests.get( 
            "https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses?filterByFormula={Phone_Number}='"+phone_number+"'",
            headers={"Authorization": str(os.environ.get("API_KEY"))})
    # Default value for response id 
    response_id = "NONE"
    if prev_response.status_code == 200:
        response_json = prev_response.json()
        for r in response_json["records"]:
            response_id = r["id"]
    return response_id