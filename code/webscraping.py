import os
import pandas as pd
import requests
import time

from bs4 import BeautifulSoup

def get_season_data(year):
    """
    Use requests and BeautifulSoup to return all relevant data for NFL players
    in the designated season.

    Keyword arguments:
    year -- season you want to pull data for
    """
    # Make page request from PFR.
    url = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'
    res = requests.get(url)

    # Create soup object out of request.
    soup = BeautifulSoup(res.content, 'lxml')

    try:
        # Extract table of player data from soup object.
        table = soup.find('table', {'id': 'fantasy'})

        # Extract all rows from table
        rows = table.find('tbody').find_all('tr')

        # Many rows in the table are just header rows, so we need to extract
        # only the rows with player information.
        player_rows = [row for row in rows if row.get('class') != ['thead']]

        return player_rows
    except AttributeError:
        return None

def extract_player_data(row):
    """
    Takes HTML row representing an NFL player and returns relevant data as a
    Python dictionary.

    Keyword arguments:
    row -- row of HTML table representing an NFL player
    """
    player = {
            'player': row.find('td', {'data-stat': 'player'}).find('a').text,
            'team': row.find('td', {'data-stat': 'team'}).text,
            'fantasy_pos': row.find('td', {'data-stat': 'fantasy_pos'}).text,
            'age': row.find('td', {'data-stat': 'age'}).text,
            'g': row.find('td', {'data-stat': 'g'}).text,
            'gs': row.find('td', {'data-stat': 'gs'}).text,
            'pass_cmp': row.find('td', {'data-stat': 'pass_cmp'}).text,
            'pass_att': row.find('td', {'data-stat': 'pass_att'}).text,
            'pass_yds': row.find('td', {'data-stat': 'pass_yds'}).text,
            'pass_td': row.find('td', {'data-stat': 'pass_td'}).text,
            'pass_int': row.find('td', {'data-stat': 'pass_int'}).text,
            'rush_att': row.find('td', {'data-stat': 'rush_att'}).text,
            'rush_yds': row.find('td', {'data-stat': 'rush_yds'}).text,
            'rush_yds_per_att': row.find(
                'td', {'data-stat': 'rush_yds_per_att'}
                ).text,
            'rush_td': row.find('td', {'data-stat': 'rush_td'}).text,
            'rec': row.find('td', {'data-stat': 'rec'}).text,
            'rec_yds': row.find('td', {'data-stat': 'rec_yds'}).text,
            'rec_yds_per_rec': row.find(
                'td', {'data-stat': 'rec_yds_per_rec'}
                ).text,
            'rec_td': row.find('td', {'data-stat': 'rec_td'}).text,
            'fumbles': row.find('td', {'data-stat': 'fumbles'}).text,
            'fumbles_lost': row.find('td', {'data-stat': 'fumbles_lost'}).text,
            'all_td': row.find('td', {'data-stat': 'all_td'}).text,
            'two_pt_md': row.find('td', {'data-stat': 'two_pt_md'}).text,
            'two_pt_pass': row.find('td', {'data-stat': 'two_pt_pass'}).text,
            'fantasy_points': row.find(
                'td', {'data-stat': 'fantasy_points'}
                ).text,
            'fantasy_points_ppr': row.find(
                'td', {'data-stat': 'fantasy_points_ppr'}
                ).text,
            'draftkings_points': row.find(
                'td', {'data-stat': 'draftkings_points'}
                ).text,
            'fanduel_points': row.find(
                'td', {'data-stat': 'fanduel_points'}
                ).text,
            'vbd': row.find('td', {'data-stat': 'vbd'}).text,
            'fantasy_rank_pos': row.find(
                'td', {'data-stat': 'fantasy_rank_pos'}
                ).text,
            'fantasy_rank_overall': row.find(
                'td', {'data-stat': 'fantasy_rank_overall'}
                ).text,
        }
    
    # Need to handle targets column individually, since before 1992 targets were
    # not tracked.
    try:
        player['targets'] = row.find('td', {'data-stat': 'targets'}).text
    except AttributeError:
        player['targets'] = None

    return player

if __name__ == '__main__':
    # Will hold data for every season we scrape.
    seasons = []

    # Get season data for most recent year.
    year = 2019
    season_data = get_season_data(year)

    # The following will run as long as there was data to scrape.
    while season_data:
        print(f'Now pulling data from {year} season')

        # Create df representing player production from the given season.
        player_data_for_season = [extract_player_data(player) for player in 
                                  season_data]
        season_df = pd.DataFrame(player_data_for_season)

        # Put columns back in the original order they came from in PFR.
        cols = list(season_df.columns)
        orig_cols_order = (
            cols[cols.index('player'): cols.index('rush_td') + 1]
            + ['targets']
            + cols[cols.index('rec'): cols.index('targets')]
        )
        season_df = season_df[orig_cols_order]

        # Add year column since we'll be scraping from many seasons.
        season_df['year'] = year

        # Add current season to season data
        seasons.append(season_df)

        # Get season data for previous year
        year -=1
        season_data = get_season_data(year)

        # Throttle server usage
        time.sleep(5)

    try:
        os.mkdir('../data')
    except FileExistsError:
        pass
    finally:
        final = pd.concat(seasons)
        final.to_csv('../data/fantasy.csv', index=False)