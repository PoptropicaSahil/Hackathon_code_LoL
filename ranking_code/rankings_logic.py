import pandas as pd
import numpy as np
from ranking_code.rs_metric_calc import create_rs_metric
from ranking_code.game_stats_calc import create_game_stats
from ranking_code.ema import ema_calc


teams_df = pd.read_parquet('data/teams_df.parquet.gzip', engine='fastparquet')



def get_ranking_list(data, date = None, ranking_types = 'global', trn_id = None, teams_list = None, msi_worlds_only = False):

    df = data.copy()
    log_messages = []

    
    if (msi_worlds_only) and (ranking_types != 'tournament'):
        log_messages.append(f'-- Running algorithm on MSI/Worlds teams')
        df = df.loc[df['useful_team_indicator'] == 1].reset_index(drop = True)
    
    elif (msi_worlds_only) and (ranking_types == 'tournament'):
        log_messages.append(f'-- Running algorithm on this MSI/Worlds tournament')
        df = df.loc[df['trn_recent_world_msi_region_22_23'] == 1].reset_index(drop = True)

    else:
        log_messages.append(f'-- Running algorithm on all teams')



    if date:
        given_date = np.datetime64(date)
        df = df.loc[df['event_date'] <= given_date].reset_index(drop = True)

        if df.shape[0] == 0:
            if msi_worlds_only: return None, f'>>> There are no MSI/Worlds games till {date}! Please enter again!', None
            return None, f'>>> There are no games till {date}! Please enter again!', None

        log_messages.append(f'-- Data filtered by date: {date}...')



    ### Tournament Rankings ###
    if ranking_types == 'tournament':

        # check if trn id entered
        if not trn_id:
            return None, f'>>> For Tournament rankings, please enter a valid Tournament ID!!', None

        trn_id = int(trn_id) # set type as int
        log_messages.append(f'-- Tournament ID entered = {trn_id}...')
        
        # Fetch Tournament name
        try:
            log_messages.append(f'-- Fetching Tournament name: {df.loc[df["Trn ID"] == trn_id]["Trn Name"].values[0]} ...')
        except:
            log_messages.append(f'-- ...')


        # check if entered trn id is present in database
        if (trn_id not in df['Trn ID'].unique()) & (msi_worlds_only):
            return None, f'>>> Entered Tournament ID {trn_id} is not a valid MSI/Worlds Tournament. \n>>> Otherwise, this ID is not available in the mapping data provided, or it does not occur till the date mentioned', None

        if trn_id not in df['Trn ID'].unique():
            return None, f'>>> Entered Tournament ID {trn_id} is invalid. \n>>> Otherwise, this ID is not available in the mapping data provided, or it does not occur till the date mentioned', None

        # not simply taking those teams performance in that trn
        # df = df.loc[df['Trn ID'] == trn_id].reset_index(drop = True)

        # chose only games upto that tournament i.e. consider historical data also
        trn_max_date = df.loc[df['Trn ID'] == trn_id]['event_date'].max()
        df = df.loc[df['event_date'] <= trn_max_date].reset_index(drop = True)

        log_messages.append(f'-- Considering games till Tournament ID {trn_id} only ...')

        # chose only teams in that tournament
        teams_in_given_trn = df.loc[df['Trn ID'] == trn_id]['Team ID'].unique().tolist()
        df = df.loc[df['Team ID'].isin(teams_in_given_trn)].reset_index(drop = True)

        log_messages.append(f'-- Chosing only teams in this Tournament ...')
        # display(df.head(3))


    ### Team Rankings ###
    elif ranking_types == 'team':

        # check if teams list entered
        if not teams_list:
            return None, f'>>> For Team rankings, please enter a list of Team IDs', None

        # check if teams in list are present in database
        total_teams = list(df['Team ID'].unique())
        teams_to_remove = []
        for team in teams_list:
            if team not in total_teams:
                teams_to_remove.append(team)
                
                try:
                    # this_team_name = df.loc[df["Team ID"] == team]["Team Name"].values[0]
                    this_team_name = teams_df.loc[teams_df['Team ID'] == team]['Team Name'].values[0]
                except:
                    this_team_name = "(name not found;')"
                if msi_worlds_only: log_messages.append(f'\t>> entered Team {this_team_name}, ID {team} is not present in MSI/Worlds database, discarding \n>>> Additionally, the team may have no matches till the entered date \n')
                else : log_messages.append(f'\t>> entered Team {this_team_name}, ID {team} is not present in database, discarding \n>>> Additionally, the team may have no matches till the entered date \n')

        eligible_teams = np.setdiff1d(teams_list, teams_to_remove).tolist()

        if len(eligible_teams) == len(teams_list):
            log_messages.append(f'-- Calculating rankings for all given teams')
        elif  len(eligible_teams) == 0:
            return None, f'>>> All entered teams have been discarded, please enter valid Team IDs \n>>> The entered teams may have no matches till the entered date', None

        df = df.loc[df['Team ID'].isin(eligible_teams)].reset_index(drop = True)

        # filter df
        pass



    ##############
    # PART A --> Generate RS Metric
    ##############
    log_messages.append(f'-- Calculating RS Metric ...')
    rs_metric_df = create_rs_metric(df)

    log_messages.append(f'-- Merging back RS Metric scores with main data ...')
    df_part_a = pd.merge(df, rs_metric_df, left_on = 'Team ID', right_on = 'team_id', how = 'left')

    df = df_part_a.copy()


    ##############
    # PART B --> Generate League importance
    # already created in the dataframe!
    ##############
    log_messages.append(f'-- Calculating League, Section, and Stage scores...')

    # 40% weight to league, 30% each to section and stage
    # df_trn_wts['league_score'] = 0.4*df_trn_wts['trn_wt'] + 0.3*df_trn_wts['section_wt'] + 0.3*df_trn_wts['stage_wt'] 

    # normalised b/w 0 and 100
    # min, max = df_trn_wts['league_score'].min(), df_trn_wts['league_score'].max()
    # df_trn_wts['league_score'] = 100*(df_trn_wts['league_score']-min)/(max-min)
    # df_trn_wts['league_score'] = df_trn_wts['league_score'].round(4)

    # df_part_b = create_league_scores(df)
    # df = df_part_b.copy()
    

    ##############
    # PART C --> Generate Game Stats
    ##############
    log_messages.append(f'-- Calculating game stats...')
    df_part_c = create_game_stats(df)
    df = df_part_c.copy()


    ##############
    # Weighted Score --> Add all game stats
    ##############
    log_messages.append(f'-- Calculating weighted score...')
    df['weighted_score'] = 0.5* df['rs_metric_norm'] + 0.30*df['league_score'] + 0.20*df['game_score_total']


    ##############
    # Post Processing --> (Exponential moving average)
    ##############
    log_messages.append(f'-- Performing Exponential Moving Average...')
    df_post_processed = ema_calc(df)


    results = df_post_processed.copy()
    results.rename(columns = {'Team Rank': f'Team Rank ({ranking_types})'}, inplace = True)

    if results['Team Name'].isnull().values.any():
        log_messages.append(f'>> Some teams have their Names, Acronyms and Slugs as None >> because their data is not given in the "teams.json" file')


    return results, None, log_messages

