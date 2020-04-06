from .models import Survey
import json
<<<<<<< HEAD

# Create the survey from JSON
=======
# Creating the survey
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
def survey_from_json(survey_json_string):
    survey_dict = json.loads(survey_json_string)
    survey = Survey()
    questions_from_json(survey, survey_json_string)
    return survey

<<<<<<< HEAD
# Add pre-determined questions to the survey from JSON
=======
# Adding the questions to the survey
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
def questions_from_json(survey, survey_json_string):
    questions_dicts = json.loads(survey_json_string).get('questions')
    for question_dict in questions_dicts:
        text = question_dict['text']
        kind = question_dict['kind']
        airtable_id = question_dict['airtable_id']
        survey.add_question(airtable_id, text, kind)
