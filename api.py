from TestMaker.TestMaker import make_test
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from generators import multiple_choice, true_false, open_ended

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the generate test url
@app.post("/generate_test")
async def generate_test(request: Request):
    # Get user data
    json_data = await request.json()
    name = json_data["name"]
    data = json_data["text"]
    question_amounts = json_data["questions"]

    # Generate Questions
    questions = []

    if question_amounts["multipleChoice"] > 0:
        for question in multiple_choice(data, question_amounts["multipleChoice"]):
            questions.append(question)
        
    if question_amounts["trueFalse"] > 0:
        for question in true_false(data, question_amounts["trueFalse"]):
            questions.append(question)

    if question_amounts["openEnded"] > 0:
        for question in open_ended(data, question_amounts["openEnded"]):
            questions.append(question)

    # Generate pdf
    pdf = make_test(name, questions)

    headers = {
        'Content-Disposition': f'inline; filename="{name}.pdf"'
    }

    # Return file to the user
    return Response(
        content=pdf, 
        media_type="application/pdf", 
        headers=headers
    )