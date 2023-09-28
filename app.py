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
    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions
    )

@app.post("/begin")
def begin():
    return redirect("/questions/0")

@app.get("/questions/<int:id>")
def questions(id):
    question = survey.questions[id]
    return render_template("question.html", question=question, id=id)

@app.post('/answer/<int:id>')
def answers(id):
    answer = request.form.get('answer')
    responses.append(answer)
    id+=1
    if id == len(survey.questions):
        #TODO: Step 5: display Q/A in a <ul>
        for question in survey.questions:
            flash(f'{question}')
        return redirect('/thankyou')

    return redirect(f'/questions/{id}')

@app.get('/thankyou')
def completion():
    return render_template('completion.html', questions=questions, answers=answers)