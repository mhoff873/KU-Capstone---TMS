from flask import render_template, request

from forms import CreateTaskForm
from app import app


@app.route('/', methods=['GET'])
def index():
    """
    Example flask-mysqldb implementation
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users''')
    NOTE: ^ is so so so so so unsecure. SQL injections yall.
    results = cursor.fetchall()
    return results

    If this lib doesn't have all the support we need, we'll need to look at
    using jQuery AJAX embedded within our python.
    """
    return render_template('index.html')


@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    steps = [1, 1]
    form = CreateTaskForm()
    if request.method == 'POST':
        if 'add_detailed' in request.form:
            steps = request.form['add_detailed']
            for i in steps:
                steps[i] = int(i)
            steps[0] += 1
            return render_template('create_task.html', form=form, num_steps=steps)
        elif 'add_main' in request.form:
            steps = request.form.getlist['add_main']
            for i in steps:
                steps[i] = int(i)
            steps[1] += 1
            return render_template('create_task.html', form=form, num_steps=steps)
        elif request.form['submit'] == 'save_as_draft':
            # User clicked save as draft button
            pass
        elif request.form['submit'] == 'publish':
            # User clicked publish button
            pass
    elif request.method == 'GET':
        return render_template('create_task.html', form=form, num_steps=steps)
