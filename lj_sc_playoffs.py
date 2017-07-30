"""
#2) BONUS: When are teams eliminated from playoff contention? Using the results for the 2016-17 regular season as a test case for your quantitative solution, please generate the date that each team was eliminated from playoff contention. We are purely looking for a date when a team was eliminated from playoff consideration, not any specific seed. Please note that your solution should generate the dates automatically, and should use code-based or Excel-based tools. To aid your work, click on this LINK for a .pdf file of the NBA Tiebreaker rules and an .xlsx file with the following three tabs 1) Divisions for the 2016-17 Season, 2) The game results for the 2016-17 NBA Regular Season, 3) A sample that includes the correct formatting for your final submission. Please note that teams that qualified for the playoffs should be labeled "Playoffs" and the date a team is eliminated should be reported in text format, not Excel Date format.

This question is not mandatory, but you are encouraged to attempt it and submit your work. Please include (at least) the following files in your zip folder: the .csv file with the dates filled in, and any code you used to generate the answer. Please separately include a brief writeup of what you did. If you used Excel to solve, please submit an Excel file in the zip folder with your work, along with your final answer in a clearly labeled tab, again with the writeup separately attached. This is a complicated problem, so we would prefer to see an incomplete solution with explanation rather than no answer.
"""

import numpy as np, pandas as pd

results = pd.read_csv('results.csv', parse_dates = ['Date'])
divisions = pd.read_csv('divisions.csv')

class team:

    def __init__(self, name, division, conference):
        self.name = name
        self.division = division
        self.conference = conference
        self.in_contention = True
        self.wins = 0
        self.losses = 0

    def percentage(self):
        try:
            return format(float(self.wins)/(self.wins + self.losses), '.3f')
        except ZeroDivisionError:
            return np.NaN

def initializeTeams():
    return {t[1]['Team_Name']: team(t[1]['Team_Name'], t[1]['Division_id'], t[1]['Conference_id']) for t in divisions.iterrows()}

def assignWL(home, away, winner):
    if winner == 'Home':
        home.wins += 1
        away.losses += 1
    else:
        home.losses += 1
        away.wins += 1

def twoWayTiebreak(A, B):
    return NotImplementedError

def multiWayTiebreak(contenders): # contenders should be a list
    return NotImplementedError

def pickWinner(home, away, winner):
    if home == winner:
        return 'Home'
    if away == winner:
        return 'Away'
    pass #come to think of it maybe this will be the day I implement a decorator

def hypothetical(date, conference=None): # Plays out the hypothetical rest of a season
    hyp_teams = initializeTeams()
    if conference != None:
        relevant_teams = dict((k, v) for k, v in hyp_teams.items() if v.conference == conference)
    df = pd.DataFrame(columns=['Wins', 'Losses', 'Percentage'], index = relevant_teams)
    for game in results[results.Date > date].iterrows():
        assignWL(hyp_teams[game[1]['Home Team']],
                 hyp_teams[game[1]['Away Team']],
                 pickWinner(hyp_teams[game[1]['Home Team']],
                            hyp_teams[game[1]['Away Team']],
                            'home'))
    for team in relevant_teams.keys():
        df.Wins[team] = hyp_teams[team].wins
        df.Losses[team] = hyp_teams[team].losses
        df.Percentage[team] = hyp_teams[team].percentage()
    return df.sort_values('Percentage', ascending=False)

def getResultsAtDate(date=None, conference=None): # includes all games before and on date
    teams = initializeTeams()
    if date == None:
        date = results.loc[len(results)-1, 'Date'] # last date in the season
    if conference != None:
        relevant_teams = dict((k, v) for k, v in teams.items() if v.conference == conference)
    df = pd.DataFrame(columns=['Wins', 'Losses', 'Percentage'], index = relevant_teams)
    for game in results[results.Date <= date].iterrows():
        assignWL(teams[game[1]['Home Team']], teams[game[1]['Away Team']], game[1]['Winner'])
    for team in relevant_teams.keys():
        df.Wins[team] = teams[team].wins
        df.Losses[team] = teams[team].losses
        df.Percentage[team] = teams[team].percentage()
    return df.sort_values('Percentage', ascending=False)

def isTeamDefinitelyOut(team, date):
    pass

team_names = initializeTeams().keys()
print(hypothetical('2016-12-04', conference='East'))








