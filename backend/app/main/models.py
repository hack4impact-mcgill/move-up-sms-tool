# Class to define survey questions
class Question():
    TEXT = 'text'
    EMAIL = 'email'

    def __init__(self, id, airtable_id, text, kind):
        self.id = id
        self.airtable_id = airtable_id
        self.text = text
        self.kind = kind

# Class to define the survey
class Survey():
    def __init__(self):
        self.questions = []

    # Adding questions to our survey
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
