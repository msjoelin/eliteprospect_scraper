
"""
Functions for collecting data from eliteprospects
Can be used together to extract data for players, matches etc. 
"""

import numpy as np
import pandas as pd
from bs4  import BeautifulSoup
import requests
import time
from datetime import datetime 

# Extract data from table - return list with rows
def tableDataText(table):
    rows = []
    trs = table.find_all('tr')

    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
        
    df_rows = pd.DataFrame(rows[1:], columns=rows[0])
    
    return df_rows


def getPlayers(league, year):  
    """
    Get all players for specific year and league; returns dataframe
    League input in format '2018-19'
    """
   
    url = 'https://www.eliteprospects.com/league/' + league + '/stats/' + year + '?page='
    # print('Collects data from ' + 'https://www.eliteprospects.com/league/' + league + '/stats/' + year)
    
    # Return list with all plyers for season in link     
    players = []
    
    for i in range(1,10):
        page = requests.get(url+str(i))        
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Get data for players table
        player_table = soup.find( "table", {"class":"table table-striped table-sortable player-stats highlight-stats season"} )
        
        if player_table is not None: 
            df_players = tableDataText(player_table)
        
            if df_players['#'].count()>0:
                # Remove empty rows
                df_players = df_players[df_players['#']!=''].reset_index(drop=True)
                
                # Extract href links in table
                href_row = []
                for link in player_table.find_all('a'):
                    href_row.append(link.attrs['href'])
                    
                # Create data frame, rename and only keep links to players
                df_links = pd.DataFrame(href_row)  
                df_links.rename(columns={ df_links.columns[0]:"link"}, inplace=True)
                df_links= df_links[df_links['link'].str.contains("/player/")].reset_index(drop=True)    
                
                # Add links to players
                df_players['link']=df_links['link'] 
                
                players.append(df_players)
                
                # Wait 3 seconds before going to next
                time.sleep(3)
    
    
    df_players = pd.concat(players).reset_index()
    
    df_players.columns = map(str.lower, df_players.columns)
    
    # Clean up dataset
    df_players['season'] = year
    df_players['league'] = league
    
    df_players = df_players.drop(['index','#'], axis=1).reset_index(drop=True)
    
    df_players['playername'] = df_players['player'].str.replace(r"\(.*\)","")
    df_players['position'] = df_players['player'].str.extract('.*\((.*)\).*')
    
    df_players['fw_def'] = df_players['position'].str.contains('LW|RW|C')
    df_players.loc[df_players['position'].str.contains('LW|RW|C'), 'fw_def'] = 'FW'
    df_players.loc[df_players['position'].str.contains('D'), 'fw_def'] = 'DEF'

    # Adjust columns; transform data
    team = df_players['team'].str.split("“", n=1, expand=True)
    df_players['team'] = team[0]
    
    # drop player-column
    df_players.drop(['player'], axis=1)
    
    return df_players


def getTeamStat(dfplayers):
    """
    Create dataframe with aggregated statistics by team, season and position (forward/defenceman) 
    Input is dataframe created with function getPlayers
    """

    dfplayers[['gp', 'g', 'a', 'tp', 'pim', '+/-']] = dfplayers[['gp', 'g', 'a', 'tp', 'pim', '+/-']].apply(pd.to_numeric, errors='coerce')

    df_teamstat = dfplayers.groupby(['team', 'season', 'fw_def'])[['gp','g', 'a', 'tp', 'pim']].sum().reset_index()

    df_teamstat['avg_g_team'] = df_teamstat['g'] / df_teamstat['gp'] 
    df_teamstat['avg_a_team'] = df_teamstat['a'] / df_teamstat['gp'] 
    df_teamstat['avg_tp_team'] = df_teamstat['tp'] / df_teamstat['gp'] 
    df_teamstat['avg_pim_team'] = df_teamstat['pim'] / df_teamstat['gp'] 

    df_teamstat['avg_+/-_team'] = dfplayers.groupby(['team', 'season', 'fw_def'])['+/-'].mean().values
    df_teamstat['nbr_players'] = dfplayers.groupby(['team', 'season', 'fw_def'])['+/-'].count().values

    return df_teamstat 


def getSeasonStat(dfplayers):
    """
    Create dataframe with aggregated statistics by season and position (forward/defenceman) 
    Input is dataframe created with function getPlayers
    """

    dfplayers[['gp', 'g', 'a', 'tp', 'pim', '+/-']] = dfplayers[['gp', 'g', 'a', 'tp', 'pim', '+/-']].apply(pd.to_numeric, errors='coerce')

    df_seasonstat = dfplayers.groupby(['season', 'fw_def'])[['gp','g', 'a', 'tp', 'pim']].sum().reset_index()

    df_seasonstat['avg_g_season'] = df_seasonstat['g'] / df_seasonstat['gp'] 
    df_seasonstat['avg_a_season'] = df_seasonstat['a'] / df_seasonstat['gp'] 
    df_seasonstat['avg_tp_season'] = df_seasonstat['tp'] / df_seasonstat['gp'] 
    df_seasonstat['avg_pim_season'] = df_seasonstat['pim'] / df_seasonstat['gp'] 

    df_seasonstat['avg_+/-_team'] = dfplayers.groupby(['season', 'fw_def'])['+/-'].mean().values
    df_seasonstat['nbr_players'] = dfplayers.groupby(['season', 'fw_def'])['+/-'].count().values

    return df_seasonstat     


def getPlayerMetadata(dfplayers):
    """
    Create dataframe with metadata by players. 
    Input is dataframe created with function getPlayers
    """
    
    # Get unique players and write to csv
    playermeta = dfplayers[['link', 'playername', 'fw_def']].drop_duplicates().reset_index(drop=True)
    
    # Make sure no players have multiple positions over seasons
    playermeta['cnt'] = playermeta.groupby(['link', 'playername'])['fw_def'].count().values
    playermeta = playermeta.sort_values(by=['link', 'playername', 'cnt'], ascending=False)
    playermeta['rank'] = playermeta.groupby(['link', 'playername']).cumcount()
    
    playermeta = playermeta[playermeta['rank']==0][['link', 'playername', 'fw_def']]
    
    return playermeta


def getPlayerStats(playerlinks): 
    """
    Takes series of playerlinks to eliteprospect-profiles, 
    Return dataframe with stats by player and season
    """    
    
    # Name of table to get data from
    tablename = "table table-striped table-condensed table-sortable player-stats skater-stats highlight-stats"
    
    data=[]
    collected_rows=0

    # Loop over all players
    for index,link in enumerate(playerlinks):

        page = requests.get(link)
        
        # Get data for player stats
        soup = BeautifulSoup(page.content, "html.parser")    
        stats_table = soup.find( "table", {"class": tablename} )

        # If html-parser didnt work  -try again
        if stats_table is None:
            soup = BeautifulSoup(page.content, "html.parser")    
            stats_table = soup.find( "table", {"class":tablename} )

        if stats_table is not None: 
            stats = tableDataText(stats_table)

            # Fill season data to include all row
            stats['S'] = stats['S'].replace('', np.nan).ffill(axis=0)
            # Add link and player data
            stats['link'] = link
            
            data.append(stats)
            collected_rows = collected_rows+len(stats)

            # Wait 3 seconds before going to next
        time.sleep(3)
        
        print(str(index+1), 'of', str(playerlinks.size), 'players imported, dataset contains', 
              str(collected_rows), 'rows', end="\r")
        
        playerStats=pd.concat(data)
        playerStats.rename(columns={ "S":"season"}, inplace=True)
       
    return playerStats


def dataprep_players(playerstats):
    """
    Takes data from players, clean it and return data frame that can be used for further analysis
    """ 
    
    # Make column names lower
    playerstats.columns = map(str.lower, playerstats.columns)
      
    #  Save relevant columns and remove rows with info about international matches
    df_stats = playerstats.copy()
    df_stats = df_stats.iloc[:,[17, 0,1,2,3,4,5,6,7,8]]
    df_stats.reset_index(drop=True)

    # Turn into numeric
    df_stats[['gp', 'g', 'a', 'tp', 'pim', '+/-']] = df_stats[['gp', 'g', 'a', 'tp', 'pim', '+/-']].apply(pd.to_numeric, errors='coerce')

    # Remove international data
    df_stats = df_stats[~df_stats['league'].str.contains("international",case=False, na=False)]

    # Mark primary team each season, where player played most games
    df_stats = df_stats.sort_values(['link', 'season', 'gp'], ascending = [True, True, False])
    
    df_stats['season_gp_rank'] = df_stats.groupby(['link', 'season']).cumcount()
    
    df_stats.loc[df_stats['season_gp_rank']==0,'primary_team'] = True
    df_stats.loc[df_stats['season_gp_rank']!=0,'primary_team'] = False
    
    df_stats = df_stats.drop(columns=['season_gp_rank'])
    
    # Filter out primary teams and add position
    df_stats_primary = df_stats[df_stats['primary_team']==True].reset_index(drop=True)
    
    df_stats_primary[['gp', 'g', 'a', 'tp', 'pim', '+/-']] = df_stats_primary[['gp', 'g', 'a', 'tp', 'pim', '+/-']].astype(dtype=np.float64)
    
    # Add metrics: Number of seasons in one league, and number of seasons in one team
    df_stats_primary['league_seasons'] = df_stats_primary.groupby(['link', 'league']).cumcount() + 1
    df_stats_primary['team_seasons'] = df_stats_primary.groupby(['link', 'team']).cumcount() + 1
    
    # Average statistics by games
    df_stats_primary['avg_g'] = df_stats_primary['g'] / df_stats_primary['gp']
    df_stats_primary['avg_a'] = df_stats_primary['a'] / df_stats_primary['gp']
    df_stats_primary['avg_tp'] = df_stats_primary['tp'] / df_stats_primary['gp']
    df_stats_primary['avg_pim'] = df_stats_primary['pim'] / df_stats_primary['gp']
    
    return df_stats_primary
    
    