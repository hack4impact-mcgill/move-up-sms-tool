from json import JSONEncoder

class Question():
    TEXT = 'text'
    EMAIL = 'email'

    def __init__(self, id, airtable_id, text, kind):
        self.id = id
        self.airtable_id = airtable_id
        self.text = text
        self.kind = kind


class Survey():
    def __init__(self):
        self.questions = []

    def add_question(self, airtable_id, text, kind=Question.TEXT):
        question = Question(len(self.questions), airtable_id, text, kind)
        self.questions.append(question)

    def first(self):
        return self.questions[0]

    def get(self, question_id):
        return self.questions[int(question_id)]

    def next(self, prev_id):
    	if int(prev_id) < len(self.questions) - 1:
        	return self.questions[int(prev_id) + 1]

# Encode Survey class to be JSON serializable
class SurveyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
