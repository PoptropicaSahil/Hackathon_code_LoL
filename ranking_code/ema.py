import pandas as pd
import numpy as np


def ema_calc(game_df):

    # ensure that the data is ordered in a way where the most recent game is at the bottom (last row) of the dataset
    game_df = game_df.sort_values(by=['year', 'month', 'day'], ascending=[True, True, True]).reset_index(drop = True)
    alpha = 0.3
    team_emas = {}
    
    for team, group in game_df.groupby('Team ID'):
        ema = group['weighted_score'].ewm(alpha=alpha, adjust=False).mean() # ema scoe for all games upto that
        ema = ema.iloc[-1] # take last value which incorporates all previous games scores
        team_emas[team] = ema

    ema_df = pd.DataFrame({'Team ID': list(team_emas.keys()), 'EMA': list(team_emas.values())})
    ema_df = ema_df.sort_values(by=['EMA'], ascending=[False]).reset_index(drop = True)
    ema_df['Team Rank'] = ema_df.index + 1 # index starts from 0


    # merge team names info to give nicer output
    team_info_df = game_df[['Team ID', 'Team Name', 'Team Acronym', 'Team Slug']].drop_duplicates()
    ema_df = pd.merge(ema_df, team_info_df, on = 'Team ID', how = 'left')
    ema_df = ema_df[['Team ID', 'Team Name', 'Team Acronym', 'Team Slug', 'EMA', 'Team Rank']]

    # if only one team given, then EMA shows as NaN --> convert to
    if ema_df.shape[0] == 1: 
        ema_df['EMA'] = 'only one team!'
    else:
        ema_df['EMA'] = ema_df['EMA'].apply(lambda x: f'{x:.6f}') # show till 6 decimals strictly

    ema_df.rename(columns = {'EMA':'Rating'}, inplace = True)


    return ema_df
