from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def home():
    """Returns start page of survey"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """Redirects to first question of survey"""

    responses.clear()

    return redirect("/questions/0")


@app.get("/questions/<int:id>")
def questions(id):
    """Returns question and selectable choices"""

    question = survey.questions[id]

    return render_template("question.html", question=question, id=id)


@app.post('/answer')
def answers():
    """Saves user response, and redirects to next page"""

    answer = request.form.get('answer')
    current_question_id = len(responses)
    next_question_id = current_question_id + 1

    responses.append(answer)

    if next_question_id == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{next_question_id}')


@app.get('/thankyou')
def completion():
    """Returns thank you page with users Q/As"""

    questions = [question.prompt for question in survey.questions]
    answers = responses
    # prompts = [{"question": questions[i], "answer": answers[i]} for i in range(len(responses))]

    return render_template('completion.html', questions=questions, answers=answers)