from . import main
from .load_data import load_question_csv
from flask import render_template, request


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/load_data', methods=['GET'])
def load_new_data():

    # Retreives the filename from the request
    filename = request.args.get('filename', type=str)
    if filename is None:
        return render_template('500.html'), 500

    else:
        num_rows = load_question_csv(filename)
        return f'Loaded {filename} successfully. Loaded {num_rows} questions into the database.'
