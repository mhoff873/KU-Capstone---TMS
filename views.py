from flask import render_template, request

from forms import CreateTaskForm
from app import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    form = CreateTaskForm()
    print(form.data)
    if form.add_main_step.data:
        print('Add main step')
        form.main_step.append_entry()
        return render_template('create_task.html', form=form)
    elif form.save_as_draft.data:
        print('Save as draft')
        return render_template('create_task.html', form=form)
    elif form.publish.data:
        print('Publish Task')
        return render_template('index.html')
    return render_template('create_task.html', form=form)
