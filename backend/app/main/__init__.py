import os
import requests
import json
from flask import Blueprint
from .parsers import survey_from_json

main = Blueprint('main', __name__) 

'''
questions = requests.get( "https://api.airtable.com/v0/appZa3BCfY1eRJCzU/Table%201",
            headers={"Authorization": str(os.environ.get("AIRTABLE_XIN_TEST_KEY"))})

if (questions.status_code == 200): 
     questions_json = questions.json()
     new_json_form = {
     "questions": [
          {
          "text": questions_json["records"][0]["fields"]["Name question"],
          "kind": "text",
          "airtable_id": "Name"
          },
          {
          "text": questions_json["records"][0]["fields"]["Email question"],
          "kind": "email",
          "airtable_id": "Email"
          }
     ],
     "title": "sign-up form"
     }
     signup_survey = survey_from_json(json.dumps(new_json_form))

else:
     with open('signup_form.json') as survey_file:
          signup_survey = survey_from_json(survey_file.read())
'''
from . import views, question_views, answer_views, survey_views


