from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def home():
    """Returns start page of survey"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """Redirects to first question of survey"""

    session['responses'] = []

    return redirect("/questions/0")


@app.get("/questions/<int:id>")
def questions(id):
    """Returns question and selectable choices"""

    if len(session['responses']) == len(survey.questions):
        flash("You've already completed the survey.")

        return redirect('/thankyou')

    current_question_id = len(session['responses'])
    if id != current_question_id:
        if id > current_question_id:
            flash("Not so fast!")
        else:
            flash("You already answered that.")

        return redirect(f'/questions/{current_question_id}')

    question = survey.questions[id]

    return render_template("question.html", question=question)


@app.post('/answer')
def answers():
    """Saves user response, and redirects to next page"""

    responses = session['responses']

    answer = request.form.get('answer')

    responses.append(answer)
    session['responses'] = responses
    next_question_id = len(responses)

    if next_question_id == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{next_question_id}')


@app.get('/thankyou')
def completion():
    """Returns thank you page with users Q/As"""

    questions = [question.prompt for question in survey.questions]
    answers = session['responses']
    # prompts = [{"question": questions[i], "answer": answers[i]} for i in range(len(responses))]

    return render_template('completion.html', questions=questions, answers=answers)