from flask import Flask, render_template, request
import sys

# C:\Users\Sahil Girhepuje\Documents\TMP\Hackathon_tries\ranking_code
# sys.path.append('/')
from ranking_code.rankings_logic import get_ranking_list
import pandas as pd

# read the file
data_path = "data/lol_database_full.parquet.gzip"
mega_data = pd.read_parquet(data_path, engine='fastparquet')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    rankings_error = None  # Error message from get_rankings function
    input_error = None     # Error message for invalid inputs
    rank_type = None
    date = None
    tournament_id = None
    team_ids_str = None
    team_ids = None
    log_messages = None
    msi_worlds_only = None

    if request.method == 'POST':
        rank_type = request.form.get('rank_type')
        date = request.form.get('date') or None
        tournament_id = request.form.get('tournament_id') or None
        team_ids_str = request.form.get('team_ids') or None
        msi_worlds_only = request.form.get('team_selection') == 'on'


        if rank_type == 'team' and team_ids_str:
            # Validate the team_ids_str
            validated_team_ids, input_error = validate_team_ids(team_ids_str)
            if input_error:
                return render_template('index.html', input_error=input_error, log_messages=log_messages
                                    #    rank_type=rank_type, date=date, tournament_id=tournament_id, team_ids=team_ids_str
                                    )
            team_ids = validated_team_ids

            
        df, rankings_error, log_messages  = get_ranking_list(data = mega_data, date = date, ranking_types = rank_type, \
                                              trn_id = tournament_id, teams_list = team_ids, msi_worlds_only = msi_worlds_only)

        if df is not None:
            data = df.to_dict(orient='records')

    # return render_template('index.html', data=data, rankings_error=rankings_error, input_error=input_error, 
    #                        log_messages=log_messages, rank_type=rank_type, date=date, 
    #                        tournament_id=tournament_id, team_ids=team_ids_str)
    return render_template('index.html', data=data, rankings_error=rankings_error, input_error=input_error,
                           log_messages=log_messages)


def validate_team_ids(team_ids_str):
    try:
        team_ids = [int(id.strip()) for id in team_ids_str.split(',')]
        return team_ids, None
    except ValueError:
        return None, "Invalid Team IDs. Please enter a comma-separated list of numbers."

if __name__ == '__main__':
    app.run(debug=True)

# def get_ranking_list(data, date = None, ranking_types = 'global', league_id = None, teams_list = None):
