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

<<<<<<< HEAD
# Regex matching to validate email address inputs
=======
# Regex matching to validate email addresses
>>>>>>> Adding and improving comments. Deleting minor redundancies/irrelevant code.
class EmailResponse(ResponseType):
    def is_valid(self, arg):
        return re.match(r'[^@]+@[^@]+\.[^@]+', arg)

# Connect db types with their corresponding objects
# for SMS instructions and validating responses
TYPE_OBJECTS = {
    Question.TEXT: TextResponse(),
    Question.EMAIL: EmailResponse(),
}
