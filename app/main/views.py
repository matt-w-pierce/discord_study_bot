from . import main
from .load_data import load_txt_file, txt_to_csv, load_csv_file
from flask import render_template, request


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/load_data', methods=['GET'])
def load_new_data():

    # Retrieves the filename from the request
    filename = request.args.get('filename', type=str)
    if filename is None:
        return render_template('500.html'), 500

    else:
        num_rows = load_txt_file(filename)
        return f'Loaded {filename} successfully. Loaded {num_rows} questions into the database.'


@main.route('/txt_to_csv', methods=['GET'])
def convert_txt_to_csv():

    # Retrieves the filename from the request
    filename = request.args.get('filename', type=str)
    if filename is None:
        return render_template('500.html'), 500

    else:
        out_file = txt_to_csv(filename)
        return f'Converted {filename} to {out_file} successfully'


@main.route('/load_existing_csv', methods=['GET'])
def load_existing_csv():

    # Retrieves the filename from the request
    filename = request.args.get('filename', type=str)
    if filename is None:
        return render_template('500.html'), 500

    else:
        num_rows = load_csv_file(filename)
        return f'Loaded {filename} successfully. Loaded {num_rows} questions into the database.'