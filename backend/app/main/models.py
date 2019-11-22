import json
from app import db
from abc import ABC, abstractmethod
from werkzeug.security import generate_password_hash, check_password_hash
import re

# create model classes here

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='survey', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    @property
    def has_questions(self):
        return self.questions.count() > 0


class Question(db.Model):
    __tablename__ = 'questions'

    TEXT = 'text'
    EMAIL = 'email'
    ENUM = 'enum'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    kind = db.Column(db.Enum(TEXT, EMAIL, ENUM, name='question_kind'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content, kind=TEXT):
        self.content = content
        self.kind = kind

    def next(self):
        return self.survey.questions\
	            .filter(Question.id > self.id)\
                    .order_by('id').first()


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    session_id = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    @classmethod
    def update_content(cls, session_id, question_id, content):
        existing_answer = cls.query.filter(Answer.session_id == session_id and
                                           Answer.question_id == question_id).first()
        existing_answer.content = content
        db.session.add(existing_answer)
        db.session.commit()

    def __init__(self, content, question, session_id):
        self.content = content
        self.question = question
        self.session_id = session_id


class ResponseType(ABC):    

    @abstractmethod
    def is_of_type(self, arg):
        pass
    
    @abstractmethod
    def instruction_text(self):
        pass


class TextResponse(ResponseType):
    def is_of_type(self, arg):
        return True

    def instruction_text(self):
        return 'Please type your answer.'


class EmailResponse(ResponseType):
    def is_of_type(self, arg):
        return re.match(r'[^@]+@[^@]+\.[^@]+', arg)

    def instruction_text(self):
        return 'Please type your answer.'


class EnumResponse(ResponseType):
    def is_of_type(self, arg):
        return True

    def instruction_text(self):
        return 'Please enter the corresponding number or text for "Other" or "Prefer not to say".'


# Connect db types with their corresponding objects
# for SMS instructions and validating responses
TYPE_OBJECTS = {
    Question.TEXT: TextResponse(),
    Question.EMAIL: EmailResponse(),
    Question.ENUM: EnumResponse()
}
