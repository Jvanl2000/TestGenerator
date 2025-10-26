# Python Imports
import os
import re

# Set Directory Variables
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "output")
file_start = open(os.path.join(current_dir, "file_header.template"), "r").read()

# Generate The Quiz
def make_quiz(quiz_name, questions):
    filename = os.path.join(output_dir, f"{quiz_name}.tex")
    with open(filename, "w", encoding="utf-8") as quiz:
        # Write the LaTeX header
        quiz.write(file_start.replace("%s", quiz_name))
        quiz.write("\\begin{questions}\n")

        # Write each question
        for question in questions:
            quiz.write(make_question(question))

        quiz.write("\\newpage\n")

        # Answer key title
        quiz.write("\\begin{center}\n")
        quiz.write("\\LARGE{\\textbf{Answer Key}}\n")
        quiz.write("\\end{center}\n")
        
        # Write the answer key
        quiz.write(make_answer_key(questions))

        # End the document
        quiz.write("\\end{questions}\n")
        quiz.write("\\end{document}")

# Parse questions for underlines
def question_parser(question):
    match = re.search(r'\$(.*?)\{(.*?)\}\$', question)
    if match:
        command = match.group(1)
        size = match.group(2)
        if command == "underline":
            question = question.replace(match.group(0), f"\\underline{{\\hspace{{{size}in}}}}")

    return question

# Generate the answer key
def make_answer_key(questions):
    answer_key = ""
    answer_key += "\\begin{questions}\n"
    for question in questions:
        answer_key += make_answer_entry(question)
    answer_key += "\\end{questions}\n"

    return answer_key

# Provide the answer key entry for a given question
def make_answer_entry(question):
    string = ""
    string += "\t\\needspace{6\\baselineskip}\n"
    
    string += f"\t\\question \n"

    if question["Type"] == "MC":
        if (type(question["Answer"]) == str):
            answer_text = question["Answer"]
        elif (type(question["Answer"]) == list):
            answer_text = ", ".join(question["Answer"])
        else:
            raise ValueError("Answer for Multiple Choice must be str or list.")

        string += f"\t{answer_text}\n"
        
    elif question["Type"] == "TF":
        string += f"\t{question['Answer']}\n"
    elif question["Type"] == "OE":
        string += f"\t{question['Answer']}\n"
    elif question["Type"] == "FIB":
        if (type(question["Answer"]) == str):
            answer_text = question["Answer"]
        elif (type(question["Answer"]) == list):
            answer_text = ", ".join(question["Answer"])
        else:
            raise ValueError("Answer for Fill in the Blank must be str or list.")

        string += f"\t{answer_text}\n"

    elif question["Type"] == "MP":
        string += "\t\\begin{parts}\n"
        for sub_question in question["Sub-Questions"]:
            string += make_answer_entry(sub_question).replace("\t", "\t\t")
        string += "\t\\end{parts}\n"

    string += "\n"

    return string

# Format the question for the test
def make_question(question):
    string = ""
    string += "\t\\needspace{6\\baselineskip}\n"
    
    if question["Point Value"] is None:
        string += f"\t\\question {question_parser(question['Question'])}\n"
    else:
        string += f"\t\\question[{question['Point Value']}] {question_parser(question['Question'])}\n"

    if question["Type"] == "MC" and len(question["Choices"]) > 0:
        string += "\t\\begin{choices}\n"
        for option in question["Choices"]:
            string += f"\t\t\\choice {option}\n"
        string += "\t\\end{choices}\n"
    elif question["Type"] == "TF":
        string += "\t\\begin{choices}\n"
        string += "\t\t\\choice {True}\n"
        string += "\t\t\\choice {False}\n"
        string += "\t\\end{choices}\n"
    elif question["Type"] == "OE":
        string += f"\t\\vspace{{{question['Spacing']}in}}\n"
    elif question["Type"] == "MP":
        string += "\t\\begin{parts}\n"
        for sub_question in question["Sub-Questions"]:
            string += make_question(sub_question).replace("\t", "\t\t")
        string += "\t\\end{parts}\n"

    string += "\n"

    return string