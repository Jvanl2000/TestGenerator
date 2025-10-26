# Python code, makes the test questions for the pdf
import random

def read_quizlet(DATA): # Gets Qs and As
    L = [] # Make a list to store the question/answer values
    i = 0
    while i < len(DATA): # Iterate through the file's list
        q = ''
        while DATA[i] != '\t': # Get the first value (question)
            q += DATA[i]
            i += 1
        i += 1
        a = ''
        while i < len(DATA) and DATA[i] != '\n': # Get the second value (answer)
            a += DATA[i]
            i += 1
        i += 1
        L.append((q, a))
    return L

def multiple_choice(DATA, n, choice_count = 4, q_type = 0): # n is the number of questions to generate, q_type is question type
    # n MUST be less than the number of Quizlet terms, or a ValueError will occur
    ORIG_DATA = read_quizlet(DATA)
    DATA = ORIG_DATA[:]
    # q_type = 0: random term/def-->def/term, 1: term-->def, 2: def-->term
    L = []
    for _ in range(n):
        L.append({"Type":"MC"})
    for D in L:
        if q_type == 0: # if random, pick a random type
            real_q_type = random.randint(1, 2)
        else:
            real_q_type = q_type
        q_num = random.randint(0, len(DATA) - 1)
        if real_q_type == 1:
            D["Question"] = "Select the corresponding answer: " + DATA[q_num][1]
            D["Answer"] = DATA[q_num][0]
            D["Choices"] = [DATA[q_num][0]]
        else:
            D["Question"] = "Select the corresponding answer: " + DATA[q_num][0]
            D["Answer"] = DATA[q_num][1]
            D["Choices"] = [DATA[q_num][1]]
        CHOICES_DATA = ORIG_DATA[:]
        del CHOICES_DATA[CHOICES_DATA.index(DATA[q_num])]
        del DATA[q_num]
        if real_q_type == 1:
            for _ in range(choice_count - 1):
                if len(CHOICES_DATA) > 0:
                    q_num = random.randint(0, len(CHOICES_DATA) - 1)
                    D["Choices"].append(CHOICES_DATA[q_num][0])
                    del CHOICES_DATA[q_num]
                else:
                    raise ValueError("Too many questions!")
        else:
            for _ in range(choice_count - 1):
                if len(CHOICES_DATA) > 0:
                    q_num = random.randint(0, len(CHOICES_DATA) - 1)
                    D["Choices"].append(CHOICES_DATA[q_num][1])
                    del CHOICES_DATA[q_num]
                else:
                    raise ValueError("Too many questions!")
        random.shuffle(D["Choices"])
        D["Point Value"] = None
    return L

def true_false(DATA, n):
    DATA = read_quizlet(DATA)
    L = [] # Initialize list
    for _ in range(n): # Initialize dictionaries
        L.append({"Type":"TF"})
    for D in L: # Finish each dictionary
        boo = random.randint(0, 1) == 0
        q_num = random.randint(0, len(DATA) - 1)
        if boo: # If answer = True, make a correct statement
            D["Question"] = "True or False: " + DATA[q_num][0] + " = " + DATA[q_num][1]
        else: # If answer = False, make an incorrect statement
            D["Question"] = "True or False: " + DATA[q_num][0] + " = "
            D["Question"] += DATA[random.randint(0, len(DATA) - 1)][1]
        D["Answer"] = str(boo) # Clarify the answer
        del DATA[q_num] # Ensures no duplicates
        D["Point Value"] = None
    return L # Return the list of dictionaries

def open_ended(DATA, n, q_type = 0, space = 0.5):
    DATA = read_quizlet(DATA)
    L = [] # Make a list to hold the questions (dictionaries)
    for _ in range(n): # Initialize the dictionaries
        L.append({"Type":"OE"})
    for D in L:
        if q_type == 0: # if random, pick a random type
            real_q_type = random.randint(1, 2)
        else:
            real_q_type = q_type
        q_num = random.randint(0, len(DATA) - 1) # chooses the order of either the first element or the second element
        if real_q_type == 1:
            D["Question"] = "Enter the definition: " + DATA[q_num][0] # Question first 
            D["Answer"] = DATA[q_num][1] # Answer second
        else:
            D["Question"] = "Enter the term: " + DATA[q_num][1] # Question second
            D["Answer"] = DATA[q_num][0] # Answer first
        D["Spacing"] = space
        D["Point Value"] = None
    return L
