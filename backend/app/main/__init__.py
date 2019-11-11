from flask import Blueprint

main = Blueprint('main', __name__) 

from . import views, question_views, answer_views, survey_views
