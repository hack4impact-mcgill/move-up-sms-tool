from flask import url_for, session, request, jsonify
import os
import requests

from twilio.twiml.messaging_response import MessagingResponse

from . import main
from .. import db
from .models import Answer, Question
from .response_types import TYPE_OBJECTS


@main.route('/answer/<question_id>/<record_id>', methods=['POST','PATCH'])
def answer(question_id,record_id):

    question = Question.query.get(question_id)

    # Verify the response matches the expected type
    # If not, prompt user
    if not is_allowed_answer(request.values['Body'], question):
        return redirect_invalid_twiml(question)

    db.save(Answer(content=request.values['Body'],
            question=question,
            session_id=session['id']))

    # Check which field name to create or update
    if question_id == '1':
        field_name = "Name"
    else:
        field_name = "Email"

    # Check if the record does not exist in the database
    if record_id == "NONE":
        temp_field = {
            "fields": {
            field_name: request.values['Body'],
            "Phone_Number": request.values['From'],
        }}
        temp_json = {"records": [temp_field]}
        # Create new record
        req = requests.post(
            'https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses',json=temp_json,
            headers={"Authorization": str(os.environ.get("API_KEY"))})

    else:
        # If the record exists in the database, update the value
        temp_field = {
            "fields": {
            field_name: request.values['Body']
        }}
        id = record_id;
        # Update record
        response = requests.patch( 
            "https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses/{}".format(id),json=temp_field,
            headers={"Authorization": str(os.environ.get("API_KEY"))})

    next_question = question.next()
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()

# Verify that the answer matches the expected type
def is_allowed_answer(body, question):
    return TYPE_OBJECTS[question.kind].is_valid(body)


# Redirect invalid answer
def redirect_invalid_twiml(question):
    response = MessagingResponse()
    response.message("Invalid response. Please try again!")
    response.redirect(url=url_for('main.question', question_id=question.id),
                      method='GET')
    return str(response)


# Redirect to the question route
def redirect_twiml(question):
    response = MessagingResponse()
    response.redirect(url=url_for('main.question', question_id=question.id),
                      method='GET')
    return str(response)


# Compose end of survey text
# TODO show all entered values and ask user to confirm
def goodbye_twiml():
    response = MessagingResponse()
    response.message("Thank you for completing the signup form! We look forward to working with you!")
    if 'question_id' in session:
        del session['question_id']
    return str(response)


