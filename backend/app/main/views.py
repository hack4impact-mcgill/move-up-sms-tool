import datetime
from flask import Flask, jsonify, request, abort, make_response, url_for, session
from twilio.twiml.messaging_response import MessagingResponse

from . import main
from .. import db
from .models import Survey, Question, Answer 


# get all users
@main.route("/", methods=["GET"])
def index():
    return "Hello World!"


# main control flow; direct user to welcome message or next question
@main.route("/message")
def sms_signup():
    response = MessagingResponse()

    signup_survey = Survey.query.first()
    if survey_error(signup_survey, response.message):
        return str(response)

    session['id'] = request.values['From']

    if 'question_id' in session:
        response.redirect(url_for('main.answer',
	                          question_id=session['question_id']))
    elif request.values.get('Body', None) == 'MOVEUP':
        redirect_to_first_question(response, signup_survey)
    else:
        welcome_user(signup_survey, response.message)
    return str(response)


@main.route('/question/<question_id>')
def question(question_id):
    question = Question.query.get(question_id)
    session['question_id'] = question.id
    return sms_twiml(question)


@main.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)

    db.save(Answer(content=extract_content(question),
            question=question,
            session_id=session['id']))

    next_question = question.next()
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()


def redirect_to_first_question(response, survey):
    first_question = survey.questions.order_by('id').first()
    first_question_url = url_for('main.question', question_id=first_question.id)
    response.redirect(url=first_question_url, method='GET')


def welcome_user(survey, send_function):
    welcome_text = 'Welcome to MoveUp\'s SMS signup tool! To continute signing up, head to their website (...) or respond MOVEUP to this message to continue here.'
    send_function(welcome_text)


def survey_error(survey, send_function):
    if not survey:
        send_function('No survey exists')
        return True
    elif not survey.has_questions:
        send_function('No questions')
        return True
    return False


def sms_twiml(question):
    response = MessagingResponse()
    response.message(question.content)
    response.message(SMS_INSTRUCTIONS[question.kind])
    return str(response)


def extract_content(question):
    return request.values['Body']


def redirect_twiml(question):
    response = MessagingResponse()
    response.redirect(url=url_for('main.question', question_id=question.id),
                      method='GET')
    return str(response)


def goodbye_twiml():
    response = MessagingResponse()
    response.message("Thank you for completing the signup form! We look forward to working with you!")
    if 'question_id' in session:
        del session['question_id']
    return str(response)


# TODO: default kinds below, will need to add more
SMS_INSTRUCTIONS = {
    Question.TEXT: 'Please type your answer',
    Question.BOOLEAN: 'Please type 1 for yes and 0 for no',
    Question.NUMERIC: 'Please type a number between 1 and 10'
}
