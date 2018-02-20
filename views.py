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
    print(request.method)
    if request.method == ['GET']:
        return render_template('create_task.html', form=form)
    # When buttons are clicked on the form, it returns a True/False value
    # We use those values to determine which buttons were clicked to add steps
    # accordingly
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
    else:
        print('Checking for detailed step button press.')
        for i, step in enumerate(form.main_step):
            print(i)
            print(step.add_detailed_step.data)
            if step.add_detailed_step.data:
                step.detailed_steps.append_entry()
                print(f'Adding detailed for main step {i}.')
    return render_template('create_task.html', form=form)
