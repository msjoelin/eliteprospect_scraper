# eliteprospect_scraper
Package to scrape ice hockey data from eliteprospect.com. 

My aim is to keep the package up-to-date so that it works also when the webpage structure is changing. 
If something is not working please reach out so that we can fix it.  

Please only use collected data for personal use - there are real APIs for professional usage of eliteprospects data.

## Getting started
Install the package with pip  
```pip install eliteprospect_scraper```

Import module
```import eliteprospect.eliteprospect_scraper as ep```

Show function descriptions with   
```help(ep)```

## Functions
Descriptions of the functions in the package.  

### getPlayers(league, year)
Get all players for a specific year and league from the page with structure
'https://www.eliteprospects.com/league/' + league + '/stats/' + year 
Example: https://www.eliteprospects.com/league/shl/stats/2016-2017

The function takes input parameters league and year 
* League: valid league [from eliteprospects](https://www.eliteprospects.com/leagues)
* year: valid combination of year in format 2015-2016, 2016-2017 etc.  

Example:  
```getPlayers('shl', '2015-2016')```  

The page contains pagination, and the function loops over 10 pages.
This is typically enough to extract all players. 

### getGoalies(league, year)
Same as getPlayers, but returns dataframe with goalies. 

### getPlayerMetadata(dfplayers)
Create dataframe with metadata by players.  
Input is dataframe created with function getPlayers 

### getPlayerStats(playerlinks)
Create dataframe with all statistics [from playerpages](https://eliteprospects.com/player/2050/mattias-ritola).  
Takes a series of playerlinks as input. Playerlinks are also included in return output from ```getPlayerMetadata``` 

```ep.getPlayerStats(["https://eliteprospects.com/player/2050/mattias-ritola"])```

### dataprep_players(playerstats, league_mapping, players):
```dataprep_players(playerstats, league_mapping, players)```
        Takes series of playerlinks to eliteprospect-profiles, 
        Return dataframe with stats by player and season


## Example Notebook
[See this notebook](https://github.com/msjoelin/eliteprospect_scraper/blob/master/sample_workbook.ipynb) for examples of how to use the package, and in what order you can run the functions. 
