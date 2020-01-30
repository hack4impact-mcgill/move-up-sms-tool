from flask import session
from twilio.twiml.messaging_response import MessagingResponse
from . import main, signup_survey

# Get the next question
@main.route('/question/<question_id>', methods=['GET'])
def question(question_id):
    question = signup_survey.get(question_id)
    session['question_id'] = question.id
    return sms_twiml(question.text)


# Generate SMS messages for the question text and instructions for responding
def sms_twiml(question_text):
    response = MessagingResponse()
    response.message(question_text)
    return str(response)
