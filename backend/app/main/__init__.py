from flask import Blueprint
from .parsers import survey_from_json

main = Blueprint('main', __name__) 

with open('signup_form.json') as survey_file:
     signup_survey = survey_from_json(survey_file.read())

from . import views, question_views, answer_views, survey_views
