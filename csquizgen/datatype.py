from enum import Enum

class DATA_TYPE(Enum):
    QUESTION = 1
    CORRECT_ANSWER  = 2
    WRONG_ANSWERS  = 3
    QUESTION_TYPE = 4 # ONLY for wooclap
    SIMPLE_QUESTION = 5 # used for quizlet and others
    CORRECT_ANSWER_INDEX = 6