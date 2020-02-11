from enum import Enum
from wooclap import WOOCLAP_QUESTION_TYPE
import random
from datatype import DATA_TYPE
from wooclap import WOOCLAP_QUESTION_TYPE
from wooclap import WOOCLAP_QUESTION
from question_util import genImportantQuestions


class BINARY_QUESTION_TYPE(Enum):
    DECIMALTOBINARY = 1
    BINARYTODECIMAL = 2
    MATCHING = 3
    SORTING = 4
    FILLBLANK = 5

BINARY_QUESTION_WOOCLAP_MAPPING = {
    BINARY_QUESTION_TYPE.DECIMALTOBINARY : WOOCLAP_QUESTION_TYPE.MCQ,
    BINARY_QUESTION_TYPE.DECIMALTOBINARY : WOOCLAP_QUESTION_TYPE.MCQ,
    BINARY_QUESTION_TYPE.MATCHING : WOOCLAP_QUESTION_TYPE.MATCHING,
    BINARY_QUESTION_TYPE.SORTING : WOOCLAP_QUESTION_TYPE.SORTING,
    BINARY_QUESTION_TYPE.FILLBLANK : WOOCLAP_QUESTION_TYPE.FILLBLANK,
}

BINARY_IMPORTANT_QUESTIONS = [
# QUESTION, SIMPLE_QUESTION, CORRECT_ANSWER, WRONG_ANSWERS(LIST)
    [
        'how many bits are a byte?',
        'a byte', 
        '8 bits', 
        ['7 bits','9 bits','10 bits']
    ],
]

# TODO add fill in the blank quesiton
"""
BINARY_EXTRA_QUESTIONS = [
# QUESTIONS, CORRECT_ANSWER, WRONG_ANSWERS(LIST)
    [
        'how many bits are a byte?',
        'a byte', 
        '8 bits', 
        ['7 bits','9 bits','10 bits']
    ],
]
"""

SUBJECT_NAME = "binary"

def genBinaryQuestions(num, data): 
    data = genBinDecConversionQuestions(num, data)
    data = genImportantQuestions(
        data,
        SUBJECT_NAME,
        BINARY_IMPORTANT_QUESTIONS
    )
    data = genSortingQuestions(data)
    data = genMatchingQuetions(data)
    return data

def genBinDecConversionQuestions(num, data):
    table = [str]*num
    for i in range(num):
        table[i] = bin(i)[2:].zfill(5)
    data[SUBJECT_NAME] = {}
    # create dec -> bin questions (starting from 2)
    data[SUBJECT_NAME][BINARY_QUESTION_TYPE.DECIMALTOBINARY] = []
    for i in range(num-2):
        while True:
            r =  random.randint(0, num)-1
            if r != i+2:
                break
        if table[r] in [table[i+2], table[i], table[i+1]]:
            randomChoice = "11111"
        else:
            randomChoice = table[r] 
        data[SUBJECT_NAME][BINARY_QUESTION_TYPE.DECIMALTOBINARY].append({
            DATA_TYPE.QUESTION_TYPE: WOOCLAP_QUESTION[WOOCLAP_QUESTION_TYPE.MCQ],
            DATA_TYPE.QUESTION: 'What is {} in binary number?'.format(i+2), # QUESTION
            DATA_TYPE.SIMPLE_QUESTION: i+2,
            DATA_TYPE.CORRECT_ANSWER: table[i+2], # CORRECZT ANSWER 
            DATA_TYPE.WRONG_ANSWERS: [
                table[i],  # WRONG ANSWER 1
                table[i+1], # WRONG ANSWER 2
                randomChoice # WRONG ANSWER 3
            ]
        })
  
    # create bin -> dec questions
    data[SUBJECT_NAME][BINARY_QUESTION_TYPE.BINARYTODECIMAL] = []
    for i in range(num-2):
        while True:
            r =  random.randint(0, num)-1
            if r != i+2:
                break
        if table[r] in [table[i+2], table[i], table[i+1]]:
            randomChoice = 31
        else:
            randomChoice = r
        data[SUBJECT_NAME][BINARY_QUESTION_TYPE.BINARYTODECIMAL].append(
            {
                DATA_TYPE.QUESTION_TYPE: WOOCLAP_QUESTION[WOOCLAP_QUESTION_TYPE.MCQ],
                DATA_TYPE.QUESTION: 'What is {} in decimal number?'.format(table[i+2]),
                DATA_TYPE.SIMPLE_QUESTION: table[i+2],
                DATA_TYPE.CORRECT_ANSWER: i+2, # CORRECZT ANSWER 
                DATA_TYPE.WRONG_ANSWERS: [
                    i, i+1, randomChoice,
                ]
            }
        )
    return data

def genSortingQuestions(data):
    # special case for Wooclap adding more questions
    # - sort 
    # 4 decimal number
    
    # 4 random binary numbers  

    # mix of binary numbers and decimal numbers

    return data

def genMatchingQuetions(data):
    # - matching
    # adding 4 random pair for each category
    # simple question - correct answer pair
    """
    random_pairs = []
    for i in range(3):
         r = random.sample(data["BINARYTODECIMAL"], 4)
         print 

    DATA_TYPE.QUESTION_TYPE: QUESTION_TYPE.MATCHING,
    DATA_TYPE.QUESTION: 'Try to match decimal and binary'.format(table[i+2]),
    SIMPLE_QUESTION: table[i+2],
        DATA_TYPE.CORRECT_ANSWER: i+2, # CORRECT ANSWER 
        DATA_TYPE.WRONG_ANSWERS: [
        i, i+1, randomChoice,
    ]
    """
    return data
