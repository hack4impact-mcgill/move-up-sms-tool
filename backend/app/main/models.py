<<<<<<< HEAD
# Class to define survey questions
=======
# A class for our survey questions
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
class Question():
    TEXT = 'text'
    EMAIL = 'email'

    def __init__(self, id, airtable_id, text, kind):
        self.id = id
        self.airtable_id = airtable_id
        self.text = text
        self.kind = kind

<<<<<<< HEAD
# Class to define the survey
=======
# A class for our survey
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
class Survey():
    def __init__(self, content, questions=[], session_id):
        self.questions = questions
        if content:
            self.content = content
        if session_id:
            self.session_id = session_id

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
<<<<<<< HEAD
        	return self.questions[int(prev_id) + 1]
<<<<<<< HEAD
=======

    def __init__(self, content, question, session_id):
        self.content = content
        self.question = question
        self.session_id = session_id
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
=======
        	return self.questions[int(prev_id) + 1]
>>>>>>> Update to pull request
