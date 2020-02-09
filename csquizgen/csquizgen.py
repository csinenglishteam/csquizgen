import sys
import csv
import random
import copy
from enum import Enum
from random import sample 
import xlsxwriter

class RECIPE(Enum):
    BINARY = 1
    LOGIC = 1

class APP(Enum):
    KAHOOT = 1
    QUIZLET = 2
    GIMKIT = 3
    WOOCLAP = 4
    GOOGLE_FORM = 5 
    # Need to enable Google form API
    # https://www.labnol.org/code/20279-import-csv-into-google-spreadsheet
    # Run App scripts

class DATA_TYPE(Enum):
    QUESTION = 1
    CORRECT_ANSWER  = 2
    WRONG_ANSWERS  = 3

DEFAULT_MAX_NUM = 32
DEFAULT_NUM_Q = 10
DEFAULT_RECIPE = RECIPE.BINARY

class OUTPUT_FORMAT_TYPE(Enum):
    CSV = 1,
    EXCEL = 2

class APP_CONFIG_TYPE(Enum):
    SAMPLE = 1
    DATA = 2
    OUTPUT_FORMAT = 3
    FILE_SUFFIX_NAME = 4

APP_CONFIG = {
    APP.WOOCLAP: {
        APP_CONFIG_TYPE.FILE_SUFFIX_NAME: "wooclap",
        APP_CONFIG_TYPE.OUTPUT_FORMAT: OUTPUT_FORMAT_TYPE.EXCEL,  
        APP_CONFIG_TYPE.SAMPLE: True,
        APP_CONFIG_TYPE.DATA : [            
            ("Type", "MCQ"),
            ("Title", DATA_TYPE.QUESTION),
            ("Correct", DATA_TYPE.CORRECT_ANSWER),
            ("Choice", DATA_TYPE.WRONG_ANSWERS),
            ("Choice", DATA_TYPE.WRONG_ANSWERS),
            ("Choice", DATA_TYPE.WRONG_ANSWERS),
        ],
    },
    APP.KAHOOT : {
        APP_CONFIG_TYPE.FILE_SUFFIX_NAME: "kahoot",
        APP_CONFIG_TYPE.OUTPUT_FORMAT: OUTPUT_FORMAT_TYPE.EXCEL,
        APP_CONFIG_TYPE.SAMPLE: True,
        APP_CONFIG_TYPE.DATA : [
            ('Question', DATA_TYPE.QUESTION),
            ('Answer 1', DATA_TYPE.CORRECT_ANSWER),
            ('Answer 2', DATA_TYPE.WRONG_ANSWERS),
            ('Answer 3', DATA_TYPE.WRONG_ANSWERS),
            ('Answer 4', DATA_TYPE.WRONG_ANSWERS),
            ('Time limit (sec)', 15),
            ('Correct answer(s)', 1),
        ],
    },
    APP.GIMKIT: {
        APP_CONFIG_TYPE.FILE_SUFFIX_NAME: "gimkit",
        APP_CONFIG_TYPE.OUTPUT_FORMAT: OUTPUT_FORMAT_TYPE.CSV,
        APP_CONFIG_TYPE.SAMPLE: False,
        APP_CONFIG_TYPE.DATA : [ 
            ("Question", DATA_TYPE.QUESTION),
            ("Correct Answer", DATA_TYPE.CORRECT_ANSWER),
            ("Incorrect Answer 1", DATA_TYPE.WRONG_ANSWERS),
            ("Incorrect Answer 2", DATA_TYPE.WRONG_ANSWERS),
            ("Incorrect Answer 3", DATA_TYPE.WRONG_ANSWERS),
        ]
    }, 
    APP.QUIZLET: {
        APP_CONFIG_TYPE.FILE_SUFFIX_NAME: "quizlet",
        APP_CONFIG_TYPE.OUTPUT_FORMAT: OUTPUT_FORMAT_TYPE.CSV,
        APP_CONFIG_TYPE.SAMPLE: True,
        APP_CONFIG_TYPE.DATA : [ 
            ("Question", DATA_TYPE.QUESTION),
            ("Correct Answer", DATA_TYPE.CORRECT_ANSWER),
        ]       
    }   
}

def main():
    if len(sys.argv)>1:
        num = int(sys.argv[1])
    else:
        num =  DEFAULT_MAX_NUM
    nQ = DEFAULT_NUM_Q
    # TODO: reading questions from csv file or json file
    data = {}
    data = genBinaryQuestions(num, data)
    output = genQuestionFiles(data, nQ)
    genFiles("binary", output)

def genBinaryQuestions(num, data): 
    table = [str]*num
    for i in range(num):
        table[i] = bin(i)[2:].zfill(5)

    # create dec -> bin questions (starting from 2)

    data["DECIMALTOBINARY"] = []
    for i in range(num-2):
        while True:
            r =  random.randint(0, num)-1
            if r != i+2:
                break
        if table[r] in [table[i+2], table[i], table[i+1]]:
            randomChoice = "11111"
        else:
            randomChoice = table[r] 
        data["DECIMALTOBINARY"].append({
            DATA_TYPE.QUESTION: 'What is {} in binary number?'.format(i+2), # QUESTION
            DATA_TYPE.CORRECT_ANSWER: table[i+2], # CORRECZT ANSWER 
            DATA_TYPE.WRONG_ANSWERS: [
                table[i],  # WRONG ANSWER 1
                table[i+1], # WRONG ANSWER 2
                randomChoice # WRONG ANSWER 3
            ]
        })
  
    # create bin -> dec questions
    data["BINARYTODECIMAL"] = []
    for i in range(num-2):
        while True:
            r =  random.randint(0, num)-1
            if r != i+2:
                break
        if table[r] in [table[i+2], table[i], table[i+1]]:
            randomChoice = 31
        else:
            randomChoice = r
        data["BINARYTODECIMAL"].append(
            {
                DATA_TYPE.QUESTION: 'What is {} in decimal number?'.format(table[i+2]),
                DATA_TYPE.CORRECT_ANSWER: i+2, # CORRECZT ANSWER 
                DATA_TYPE.WRONG_ANSWERS: [
                    i, i+1, randomChoice,
                ]
            }
        )
    return data

def genQuestionFiles(data, nQ):
    questions = []
    filtered_questions = []
    nCat = len(data.keys())
    for k, d in data.items():
        questions.extend(d)
        filtered_questions.extend(sample(d, int(nQ/nCat)))

    output = {}
    for app, config in APP_CONFIG.items():
        print(app)
        output[app] = [] 
        row = []
        for c in config[APP_CONFIG_TYPE.DATA]:
            row.append(c[0])
        output[app].append(row)
        if config[APP_CONFIG_TYPE.SAMPLE]:
            q = filtered_questions
        else:
            q = questions
        for question in q:
            wrong_answers = copy.deepcopy(question[DATA_TYPE.WRONG_ANSWERS])
            row = []
            for p in config[APP_CONFIG_TYPE.DATA]:
                if type(p[1]) == DATA_TYPE:
                    if p[1] == DATA_TYPE.WRONG_ANSWERS:
                        wrong_answer = random.choice(wrong_answers)
                        row.append(wrong_answer)
                        wrong_answers.remove(wrong_answer)
                    else:
                        row.append(question[p[1]])
                else:
                    row.append(p[1])
            output[app].append(row)
    return output
    
def genFiles(filename, output):
    for app, data in output.items():
        file_suffix = APP_CONFIG[app][APP_CONFIG_TYPE.FILE_SUFFIX_NAME] 
        if (APP_CONFIG[app][APP_CONFIG_TYPE.OUTPUT_FORMAT] 
            == OUTPUT_FORMAT_TYPE.EXCEL):
            workbook = xlsxwriter.Workbook(filename+"_"+file_suffix+".xlsx")
            worksheet = workbook.add_worksheet()
            for row_num, row in enumerate(data):
                for col_num, d in enumerate(row):
                    worksheet.write(row_num, col_num, d)
            workbook.close()
        elif (APP_CONFIG[app][APP_CONFIG_TYPE.OUTPUT_FORMAT] 
            == OUTPUT_FORMAT_TYPE.CSV):
            with open(filename+"_"+file_suffix+".csv", "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)          

if __name__== "__main__":
  main()