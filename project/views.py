from flask import render_template

from project import app
from project.forms import CreateTaskForm


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


@app.route('/create_task/', methods=['GET'])
def create_task():
    form = CreateTaskForm()
    return render_template('create_task.html', form=form)
