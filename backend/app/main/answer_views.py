from flask import url_for, session, request
from twilio.twiml.messaging_response import MessagingResponse

from . import main
from .. import db
from .models import Answer, Question, EnumResponse, TYPE_OBJECTS


@main.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)

    # Verify the response matches the expected type
    # If not, prompt user
    if not is_allowed_answer(request.values['Body'], question):
        return redirect_invalid_twiml(question)
	
    if question.kind is Question.ENUM:
        answer_body = EnumResponse(question).map_value(request.values['Body'])
    else:
        answer_body = request.values['Body']

    db.save(Answer(content=answer_body,
            question=question,
            session_id=session['id']))

    next_question = question.next()
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()


# Verify that the answer matches the expected type
def is_allowed_answer(body, question):
    if question.kind is Question.ENUM:
        return EnumResponse(question).is_of_type(body)
    else:
        return TYPE_OBJECTS[question.kind].is_of_type(body)


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
