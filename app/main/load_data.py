import os
import pandas as pd
from .. import db
from ..models import Question


def load_txt_file(txt_file):
    """
    Converts the text file to a CSV and loads the CSV file data into the database
    :param txt_file: Name of the file to be converted and loaded
    :return: Return value from load_csv_file function
    """
    base_path = 'data_files'

    # Converts the text file to a CSV file
    csv_file = txt_to_csv(txt_file, base_path)
    data_len = load_csv_file(csv_file, base_path)
    return data_len


def txt_to_csv(in_file, base_path='data_files'):
    """
    Reads in a text file with '<!>' as row separators and '|' as column separators and converts to CSV file
    :param base_path: Path to the data file directory
    :param in_file: Name of the text file to read in
    :return: CSV file name
    """
    in_path = os.path.join(base_path, in_file)

    out_file = f'{os.path.splitext(in_file)[0]}.csv'
    out_path = os.path.join(base_path, out_file)

    txt_in = open(in_path, 'rt')
    txt_out = open(out_path, 'wt')
    txt_out.write('"prompt","answer"\n')

    lines = txt_in.readlines()
    # print(f'Number of lines: {len(lines)}')
    for i, line in enumerate(lines):

        # Removing any instances of double-quotes with single quotes
        line = line.replace('"', "'")

        # The first line needs a leading double quote
        if i == 0:
            line = '"' + line

        # Replacing custom delimiters with quote bound CSV delimiters
        line = line.replace('|', '","')
        line = line.replace('<!>', '"\n"')

        # If it is the last line, then we don't need the closing quote, which is the last character
        if i == (len(lines) - 1):
            line = line[:-1]

        # Writing the line to the output file
        txt_out.write(line)

    # Closing input and output files
    txt_in.close()
    txt_out.close()

    return out_file


def load_csv_file(csv_file, base_path='data_files'):
    """
    Reads in the provided CSV file and stores the data in the MySQL database
    :param base_path: Path to the data file directory
    :param csv_file: Name of the text file that should be read in
    :return: Length of the data loaded
    """

    # Locates the CSV file, loads into a dataframe and then converts into a list of dicts
    df = pd.read_csv(os.path.join(base_path, csv_file))
    set_name = csv_file[:-4]
    df['set_name'] = set_name
    data = df.T.to_dict().values()

    # Deleting all rows with this set_name from the database before loading
    Question.query.filter_by(set_name=set_name).delete()
    # delete_query = Question.query.filter_by(set_name=set_name).delete()
    # db.session.delete(delete_query)
    db.session.commit()

    # Adding the data back to the database
    for d in data:
        q = Question.from_dict(d)
        db.session.add(q)

    db.session.commit()
    return len(data)
