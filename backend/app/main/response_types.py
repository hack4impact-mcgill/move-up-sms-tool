from abc import ABC, abstractmethod
import re
from .models import Question

class ResponseType(ABC):    
    @abstractmethod
    def is_valid(self, arg):
        pass
    
class TextResponse(ResponseType):
    def is_valid(self, arg):
        return True

# Regex matching to validate email address inputs
class EmailResponse(ResponseType):
    def is_valid(self, arg):
        return re.match(r'[^@]+@[^@]+\.[^@]+', arg)

# Connect db types with their corresponding objects
# for SMS instructions and validating responses
TYPE_OBJECTS = {
    Question.TEXT: TextResponse(),
    Question.EMAIL: EmailResponse(),
}
