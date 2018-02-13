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
    if request.method == 'GET':
        form = CreateTaskForm()
        return render_template('create_task.html', form=form)
    elif request.form['submit'] == 'save_as_draft':
        # User clicked save as draft button
        pass
    elif request.form['submit'] == 'publish':
        # User clicked publish button
        pass
