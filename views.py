from flask import render_template, request

from forms import CreateTaskForm
from app import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    num_detailed_steps = 1
    form = CreateTaskForm()
    if request.method == 'POST':
        action = request.form['submit']
        if action == 'save_as_draft':
            # User clicked save as draft button
            pass
        elif action == 'publish':
            # User clicked publish button
            pass
        elif action == 'add_main_step':
            print(f'Current number of main steps: {len(form.main_step.entries)}')
            print('Adding main step.')
            form.main_step.append_entry()
            print(f'New number of main steps: {len(form.main_step.entries)}')
            return render_template('create_task.html', form=form)
    elif request.method == 'GET':
        return render_template('create_task.html', form=form)
