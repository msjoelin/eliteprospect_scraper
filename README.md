# eliteprospect_scraper
Package to scrape hockey data from eliteprospect.  
Please only use collected data for personal use - there are real APIs for professional usage of eliteprospects data.

## Getting started
Package can be installed with pip  
```pip install eliteprospect_scraper```

In python, import module with  
```import eliteprospect.eliteprospect_scraper as ep```

See description of functions in package with  
```help(ep)```

Functions can be used together and input and output is linked. 

## Functions
Description of functions contained in package. Ordered in 

### getPlayers(league, year)
Get all players for specific year and league; returns dataframe. 
* League: valid league [from eliteprospects](https://www.eliteprospects.com/leagues)
* year: valid combination of year in format 2015-16, 2016-17 etc.  

Example:  
```getPlayers('shl', '2015-16')```  

### getPlayerMetadata(dfplayers)
Create dataframe with metadata by players.  
Input is dataframe created with function getPlayers 

### getPlayerStats(playerlinks)
Create dataframe with all statistics [from playerpages](https://eliteprospects.com/player/2050/mattias-ritola).  
Takes series of playerlinks as input. Playerlinks are also included in return output from ```getPlayerMetadata``` 

```ep.getPlayerStats(["https://eliteprospects.com/player/2050/mattias-ritola"])```

### dataprep_players(playerstats, league_mapping, players):

```help(ep)```
 dataprep_players(playerstats, league_mapping, players)
        Takes series of playerlinks to eliteprospect-profiles, 
        Return dataframe with stats by player and season


## How to use
See this notebook for examples of how to use the package, and in what order you can run the functions. 
