import pandas as pd
import numpy as np


def create_game_stats(game_df):

    # XP
    def xp_score(row):
        if row['xp_own_avg'] < 9000: return 15.5
        elif 9000 <= row['xp_own_avg'] < 19000: return 22.5
        else: return 32.5
    game_df['xp_score'] = game_df.apply(xp_score, axis=1)

    # Attack Speed
    def attack_speed_score(row):
        if row['attackSpeed_own_avg'] < 140: return 0.75
        elif 140 <= row['attackSpeed_own_avg'] < 210: return 1.5
        else: return 2.5
    game_df['attack_speed_score'] = game_df.apply(attack_speed_score, axis=1)

    # Champion kills
    def champ_kills_score(row):
        if row['championsKills_own'] < 10: return 7.5
        elif 10 <= row['championsKills_own'] < 30: return 15
        else: return 25
    game_df['champ_kills_score'] = game_df.apply(champ_kills_score, axis=1)

    # Total Gold
    def total_gold_score(row):
        if row['totalGold_own'] < 40000: return 7.5
        elif 40000 <= row['totalGold_own'] < 80000: return 15
        else: return 25
    game_df['total_gold_score'] = game_df.apply(total_gold_score, axis=1)

    # Avg Level
    def level_own_score(row):
        if row['level_own_avg'] < 11: return 1
        elif 11 <= row['level_own_avg'] < 13: return 2
        elif 13 <= row['level_own_avg'] < 15: return 3
        elif 15 <= row['level_own_avg'] < 17: return 4
        else: return 5
    game_df['level_own_score'] = game_df.apply(level_own_score, axis=1)

    # Diff in Level
    def level_diff_score(row):
        if (row['level_own_avg'] - row['level_opp_avg']) > 2:  # One sided match and I am stronger
            if row['Outcome'] == 1: return 6 # win
            else: return 1 # lose

        elif (row['level_own_avg'] - row['level_opp_avg']) < -2:  # One sided match and I am weaker
            if row['Outcome'] == 1: return 10 # win
            else: return 4 # lose

        else: # Equal match
            if row['Outcome'] == 1: return 8 # win
            else: return 5 # lose

    game_df['level_diff_score'] = game_df.apply(level_diff_score, axis=1)

    # Calc total game score
    game_df['game_score_total'] = game_df['xp_score'] + game_df['attack_speed_score'] + game_df['champ_kills_score'] + \
                                    game_df['total_gold_score'] + game_df['level_own_score'] + game_df['level_diff_score']

    return game_df


