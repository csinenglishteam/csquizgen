from wooclap import WOOCLAP_QUESTION_TYPE
from wooclap import WOOCLAP_QUESTION
from datatype import DATA_TYPE
from enum import Enum

class SHARED_QUESTION_TYPE(Enum):
    IMPORTANT = 1

def genImportantQuestions(data, subjectName, extraQuestions):
    data[subjectName][SHARED_QUESTION_TYPE.IMPORTANT] = []
    for q in extraQuestions:
        data[subjectName][SHARED_QUESTION_TYPE.IMPORTANT].append(
            {
                DATA_TYPE.QUESTION_TYPE: WOOCLAP_QUESTION[WOOCLAP_QUESTION_TYPE.MCQ],
                DATA_TYPE.QUESTION: q[0],
                DATA_TYPE.SIMPLE_QUESTION: q[1],
                DATA_TYPE.CORRECT_ANSWER: q[2], # CORRECZT ANSWER 
                DATA_TYPE.WRONG_ANSWERS: q[3]
            } 
        )
    return data