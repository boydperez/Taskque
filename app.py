from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfjsd832rhwjf9723hfue'

class CreateTaskForm(FlaskForm):
    title = StringField('Task', validators=[DataRequired()])
    content = TextAreaField('Task Description')
    submit = SubmitField('')



@app.route('/', methods=['POST', 'GET'])
def home():
    tasks = request.cookies
    return render_template('index.html', tasks=tasks)

@app.route('/createtask', methods=['POST', 'GET'])
def createTask():
    form = CreateTaskForm()
    if form.validate_on_submit():
        # global tasks
        task = request.form.get('title')
        task_description = request.form.get('content')

        res = make_response(redirect(url_for('home')))
        res.set_cookie(task, task_description, max_age=60*60*24*365) 
        return res
    return render_template('createtask.html', form=form)

@app.route('/updatetask/<title>', methods=['POST', 'GET'])
def updateTask(title):
    form = CreateTaskForm()
    form.title.data = title 
    form.content.data = request.cookies.get(title)
    if form.validate_on_submit():
        task = request.form.get('title')
        task_description = request.form.get('content')
        res = make_response(redirect(url_for('home')))
        res.set_cookie(title, max_age=0)
        res.set_cookie(task, task_description, max_age=60*60*24*365)
        return res
    return render_template('updatetask.html', form=form)


@app.route('/deletetask/<title>')
def deleteTask(title):
    res = make_response(redirect(url_for('home')))
    res.set_cookie(title, max_age=0)
    return res
