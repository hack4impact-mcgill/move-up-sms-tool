from flask import session
from twilio.twiml.messaging_response import MessagingResponse

from . import main
from .models import Question, TYPE_OBJECTS

# Get the next question
@main.route('/question/<question_id>', methods=['GET'])
def question(question_id):
    question = Question.query.get(question_id)
    session['question_id'] = question.id
    return sms_twiml(question)



# Generate SMS messages for the question text and instructions for responding
def sms_twiml(question):
    response = MessagingResponse()
    response.message(question.content)
    response.message(TYPE_OBJECTS[question.kind].instruction_text())
    return str(response)
