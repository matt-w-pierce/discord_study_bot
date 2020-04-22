import os
import pandas as pd
from .. import db
from ..models import Question


def load_question_csv(filename):

    # Locates the CSV file, loads into a dataframe and then converts into a list of dicts
    df = pd.read_csv(os.path.join('app', 'data_files', filename))
    set_name = filename[:-4]
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
