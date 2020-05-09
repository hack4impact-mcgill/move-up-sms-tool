from flask import url_for, session, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import json
from .parsers import survey_from_json
import jsonpickle
from . import main

# Main control flow: direct user to welcome message or next question
@main.route('/message', methods=['GET'])
def sms_signup():
    response = MessagingResponse()    
    questions = requests.get( "https://api.airtable.com/v0/appZa3BCfY1eRJCzU/Table%201",
            headers={"Authorization": str(os.environ.get("AIRTABLE_XIN_TEST_KEY"))})

    if (questions.status_code == 200): 
        questions_json = questions.json()
        new_json_form = {
        "questions": [
        ],
        "title": "sign-up form"
        }
        for (key, value) in questions_json["records"][0]["fields"].items():
            kind = "email" if key == "Email" else "text",
            new_question = {
            "text": value,
            "kind": kind,
            "airtable_id": key
            }
            new_json_form["questions"].insert(0, new_question)
        # End of question retrieval

        # Encoding survey so it is JSON serializable in order to be stored in the session    
        session["signup_survey"] = jsonpickle.encode(survey_from_json(json.dumps(new_json_form)))

    else:
        with open('signup_form.json') as survey_file:
            session["signup_survey"] = jsonpickle.encode(survey_from_json(survey_file.read()))

    # Retrieving the survey from the session requires it to be decoded
    if survey_error(jsonpickle.decode(session["signup_survey"]), response.message):
        return str(response)
    
    body = request.values.get('Body', None)
    if body: body = body.strip()

    # Retrieve the client's phone number and format it
    phone_number = "%2B" + request.values.get('From', " ")[1: ] 

    if 'question_id' in session:    
        # Retrieve the record id to check if the client registered before
        response_id = retrieve_prev_record(phone_number)
        # Redirect the response to the answer-saving url
        answer_url = url_for('main.answer', question_id=session['question_id'], record_id=response_id)
        response.redirect(url=answer_url)
    elif body == 'SIGNUP':
        redirect_to_first_question(response, jsonpickle.decode(session["signup_survey"]))
    elif body == 'MOVEUP':
        welcome_user(response.message, (retrieve_prev_record(phone_number)=="NONE"))
    else:
        response.message(None)
    return str(response)
    response.message(None)
    return str(response)


# Catch survey errors
def survey_error(survey, send_function):
    if not survey:
        send_function('No survey exists')
        return True
    elif not survey.first():
        send_function('No questions')
        return True
    return False


# Route the user to the first question
def redirect_to_first_question(response, survey):
    first_question = survey.first()
    first_question_url = url_for('main.question', question_id=first_question.id)
    response.redirect(url=first_question_url, method='GET')


# Send a welcome message to the user
def welcome_user(send_function, is_prev_response=False):
    if not is_prev_response:
        welcome_text = 'Welcome to Move Up! To sign up and get paired with a mentor, you can either continue here or head to our online form (https://bit.ly/moveup-signup). To continue here, please respond SIGNUP.'
    else:
        welcome_text = 'It appears as though we already have a response from you. If you would like to update your information, please respond SIGNUP. Otherwise, we will keep your current information as is.'
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
