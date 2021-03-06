from flask import url_for, session, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import jsonpickle
from . import main
from .response_types import TYPE_OBJECTS
from config import config

@main.route('/answer/<question_id>/<record_id>', methods=['POST','PATCH'])
def answer(question_id, record_id):

    question = jsonpickle.decode(session["signup_survey"]).get(question_id)

    # Verify the response matches the expected type
    # If not, prompt user

    if not is_allowed_answer(request.values['Body'], question.kind):
        return redirect_invalid_twiml(question.id)
    # Check the record id to see if the client's information exists in the Airtable
    if record_id == "NONE":
        # If not, create a record for them
        create_airtable_record(request.values['From'], question.airtable_id, request.values['Body'])
    else:
        # If so, we update their record
        update_airtable_record(record_id, question.airtable_id, request.values['Body'])
    next_question = jsonpickle.decode(session["signup_survey"]).next(question_id)
    if next_question:
        # If survey is not completed, ask the next question
        return redirect_twiml(next_question.id)
    else:
        # Otherwise, send goodbye / thank you message
        return goodbye_twiml()

# Verify that the answer matches the expected type
def is_allowed_answer(body, question_kind):
    return TYPE_OBJECTS[question_kind].is_valid(body)

# Redirect invalid answer
def redirect_invalid_twiml(question_id):
    response = MessagingResponse()
    response.message("Invalid response. Please try again!")
    response.redirect(url=url_for('main.question', question_id=question_id), method='GET')
    return str(response)

# Redirect to the question route
def redirect_twiml(question_id):
    response = MessagingResponse()
    response.redirect(url=url_for('main.question', question_id=question_id), method='GET')
    return str(response)

# Compose end of survey text
# TODO change message as per conversation with MoveUp
def goodbye_twiml():
    response = MessagingResponse()
    response.message("Thank you for completing the form. We will reach out to you shortly with next steps. We look forward to working with you.")
    if 'question_id' in session:
        del session['question_id']
    return str(response)

# Update the client's previous record in the Airtable
def update_airtable_record(record_id, field_name, field_value):
    temp_field = {
        "fields": {
        field_name: field_value
    }}
    requests.patch( 
            "{}/{}".format(config[os.getenv("FLASK_CONFIG")].DATABASE_URL, record_id),json=temp_field,
            headers={"Authorization": str(os.environ.get("API_KEY"))})

# Create a new record in the Airtable for the client and store their phone numbers
def create_airtable_record(phone_num, field_name, field_value):
    temp_field = {
        "fields": {
        field_name: field_value,
        "Phone_Number": phone_num,
    }}
    temp_record = {"records": [temp_field]}
    requests.post(
        config[os.getenv("FLASK_CONFIG")].DATABASE_URL, json=temp_record,
        headers={"Authorization": str(os.environ.get("API_KEY"))})
