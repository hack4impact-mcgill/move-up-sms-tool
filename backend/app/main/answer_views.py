from flask import url_for, session, request, jsonify
# My imports
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

    
    #Store it in the Airtable
    if question_id == '1':
        field_name = "Name"
    else:
        field_name = "Email"
    
    temp_info = {
        field_name: request.values['Body'],
    }
    temp_field = {"fields": temp_info}
    temp_json = {"records": [temp_field]}

   # headers = {'Authorization': 'Bearer keybp9BmMeD5OLIjq', 'Content-Type': 'application/json; charset=utf-8'}
    req = requests.post('https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses',json=temp_json,headers={"Authorization": str(os.environ.get("API_KEY"))})
    response_json = req.json()
    
    for r in response_json["records"]:
        row_id = r["id"]

    next_question = question.next()
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()

#My own route
@main.route('/test', methods=['GET'])
def test():
    #To Store information in Airtable
    temp_info = {
        "Email": "madonna197@outlook.com",
    }
    temp_field = {"fields": temp_info}
    temp_json = {"records": [temp_field]}

   # headers = {'Authorization': 'Bearer keybp9BmMeD5OLIjq', 'Content-Type': 'application/json; charset=utf-8'}
    req = requests.post('https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses',json=temp_json,headers={"Authorization": str(os.environ.get("API_KEY"))})
    response_json = req.json()
    
    for r in response_json["records"]:
        row_id = r["id"]

    return str(row_id)

@main.route('/test_get_phone', methods=['GET'])
def test_get_phone():
    #To see if the client is already in the airtable
    name = "%2B15147469875"
    # .format('FIND("Madonna",{name})')
    #{Email}='514'
    response = requests.get( 
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/SMS%20Responses?filterByFormula={Phone_Number}='"+name+"'",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    response_id = ""
    if response.status_code ==200:
        response_json = response.json()
        for r in response_json["records"]:
            response_id = r["id"]
    
    return str(response_id)

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


