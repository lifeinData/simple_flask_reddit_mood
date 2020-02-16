from flask import Flask, request, abort
import Constants.SQL_QUERIES as query_constants
import pandas as pd
import sys
import REST.aggregations_by_sub.Get

#TODO: Make into environment variable
sys.path.append('../reddit_mood_bot')
from Scripts.database.query_executors import db_execution_objs as db_func

# !flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)
cursor = db_func.get_db_funct_object()[0]


def get_json_form(subred):
    cursor.execute(query_constants.SELECT_GROUPED_EMOTIONS, [subred])
    data = cursor.fetchall()
    relevant_col = ['subred', 'ang', 'anti', 'dis', 'fear', 'joy', 'sad', 'surp', 'trus']
    df1 = pd.DataFrame(data, columns=relevant_col)
    df1['t'] = df1['ang'] + df1['anti'] + df1['dis'] + df1['fear'] + df1['joy'] + df1['sad'] + df1['surp'] + df1['trus']

    for c in df1.columns:
        if c != 't' and c != 'subred':
            df1[c] = round(df1[c] / df1['t'], 2) * 100

    df1[relevant_col[1:]] = df1[relevant_col[1:]].astype(
        int)  # convert the emotion only columns to int so that it shows up right as a json
    df_json = df1[df1['subred'] == subred][relevant_col].to_json(orient='records')

    return df_json[1:-1]  # get rid of the [] characters


@app.route('/reddit_mood/rest/get_emotion_aggregations/<string:subred>', methods=['GET'])
def get_json_aggregations(subred):
    json = get_json_form(subred)
    if len(json) == 0:
        abort(404)
    return json

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
