from flask import session
from twilio.twiml.messaging_response import MessagingResponse

from . import main
from .models import Question

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
    response.message(SMS_INSTRUCTIONS[question.kind])
    return str(response)


# Sample instruction texts for different types of questions
# TODO add any missing ones
# TODO verify that answers conform to the question type
SMS_INSTRUCTIONS = {
    Question.TEXT: 'Please type your answer',
    Question.BOOLEAN: 'Please type 1 for yes and 0 for no',
    Question.NUMERIC: 'Please type a number between 1 and 10'
}
