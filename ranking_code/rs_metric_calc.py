import pandas as pd
import numpy as np

def create_rs_metric(table_df):

    def calc_rs_metric_by_bucket(row):
        if row['num_games'] < 20:
            return 0.1 * row['num_games'] + 0.5*row['wins_pct']
        elif 21 <= row['num_games'] < 150:
            return 0.15 * row['num_games'] + 1.5*row['wins_pct']
        else :
            return 0.15 * row['num_games'] + 0.75*row['wins_pct']

    team_stats_list = []
    for team_id, team_df in table_df.groupby('Team ID'):
        num_games = team_df["Game ID"].nunique()
        num_wins = (team_df["Outcome"] == 'win').sum()
        num_loss = (team_df["Outcome"] == 'loss').sum()
        wins_pct = 100*(num_wins/num_games).round(4)
        team_stats_list.append([team_id, num_games, num_wins, num_loss, wins_pct])

    team_stats = pd.DataFrame(team_stats_list, columns=["team_id", "num_games", "num_wins", "num_loss", "wins_pct"])
    team_stats['rs_metric'] = team_stats.apply(calc_rs_metric_by_bucket, axis=1)

    # normalise between 0 to 100
    col_min, col_max = team_stats['rs_metric'].min(), team_stats['rs_metric'].max()
    team_stats['rs_metric_norm'] = ( team_stats['rs_metric'] - col_min ) / ( col_max - col_min )
    team_stats['rs_metric_norm'] = 100*team_stats['rs_metric_norm'].round(5)

    return team_stats
