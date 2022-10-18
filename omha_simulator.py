import scipy.stats
import numpy as np
import random
import pandas as pd
import time

class Team():
    def __init__(self, name, rating, wins=0, losses=0, ties=0, points=0, goals_for=0, goals_against=0, teams_beat=[], teams_lost_to=[], teams_tied=[]):
        self.name = name
        self.rating = float(rating)
        self.wins = int(wins)
        self.losses = int(losses)
        self.ties = int(ties)
        self.points = int(points)
        self.goals_for = int(goals_for)
        self.goals_against = int(goals_against)
        self.teams_beat = []
        self.teams_lost_to = []
        self.teams_tied = []

class Game():
    def __init__(self, home, away, tie=True, standard_deviation=2.39):
        self.home = home
        self.away = away
        self.tie = bool(tie)
        self.standard_deviation = float(standard_deviation)

    def simulate(self):
        if self.tie == True:
            goal_differential = round(np.random.normal(self.home.rating-self.away.rating,self.standard_deviation))

            home_goals = round(abs(np.random.normal(2.84,2.18))+(goal_differential/2))
            away_goals = home_goals - goal_differential
            if home_goals >= 0 and away_goals >= 0:
                pass
            else:
                if goal_differential > 0:
                    home_goals = goal_differential
                    away_goals = 0
                elif goal_differential == 0:
                    home_goals = 0
                    away_goals = 0
                elif goal_differential < 0:
                    home_goals = 0
                    away_goals = abs(goal_differential)

            self.home.goals_for += home_goals
            self.home.goals_against += away_goals
            self.away.goals_for += away_goals
            self.away.goals_against += home_goals

            if goal_differential > 0:
                self.home.wins += 1
                self.away.losses += 1
                self.home.points += 2
                self.home.teams_beat.append(self.away)
                self.away.teams_lost_to.append(self.home)
                return {'Winner': self.home, 'Loser': self.away, 'Differential': goal_differential, 'Home Goals': home_goals, 'Away Goals': away_goals}
            elif goal_differential == 0:
                self.home.ties += 1
                self.away.ties += 1
                self.home.points += 1
                self.away.points += 1
                self.home.teams_tied.append(self.away)
                self.away.teams_tied.append(self.home)
                return {'Winner': None, 'Loser': None, 'Differential': goal_differential, 'Home Goals': home_goals, 'Away Goals': away_goals}
            elif goal_differential < 0:
                self.home.losses += 1
                self.away.wins += 1
                self.away.points += 2
                self.home.teams_lost_to.append(self.away)
                self.away.teams_beat.append(self.home)
                return {'Winner': self.away, 'Loser': self.home, 'Differential': goal_differential, 'Home Goals': home_goals, 'Away Goals': away_goals}

        elif self.tie == False:
            goal_differential = np.random.normal(self.home.rating-self.away.rating,self.standard_deviation)

            home_goals = round(abs(np.random.normal(2.84,2.18))+(goal_differential/2))
            away_goals = home_goals - round(goal_differential)
            if home_goals >= 0 and away_goals >= 0:
                pass
            else:
                if goal_differential > 0:
                    home_goals = goal_differential
                    away_goals = 0
                elif goal_differential == 0:
                    home_goals = 0
                    away_goals = 0
                elif goal_differential < 0:
                    home_goals = 0
                    away_goals = round(abs(goal_differential))

            self.home.goals_for += home_goals
            self.home.goals_against += away_goals
            self.away.goals_for += away_goals
            self.away.goals_against += home_goals

            if goal_differential > 0:
                self.home.wins += 1
                self.away.losses += 1
                self.home.points += 2
                self.home.teams_beat.append(self.away)
                self.away.teams_lost_to.append(self.home)
                return {'Winner': self.home, 'Loser': self.away, 'Differential': round(goal_differential), 'Home Goals': home_goals, 'Away Goals': away_goals}
            elif goal_differential == 0: #should almost never happen
                if random.randint(0,1) == 0:
                    self.home.wins += 1
                    self.away.losses += 1
                    self.home.points += 1
                    self.away.points += 1
                    self.home.teams_beat.append(self.away)
                    self.away.teams_lost_to.append(self.home)
                    return {'Winner': self.home, 'Loser': self.away, 'Differential': round(goal_differential), 'Home Goals': home_goals, 'Away Goals': away_goals}
                else:
                    self.home.losses += 1
                    self.away.wins += 1
                    self.home.points += 1
                    self.away.points += 1
                    self.home.teams_lost_to.append(self.away)
                    self.away.teams_beat.append(self.home)
                    return {'Winner': self.away, 'Loser': self.home, 'Differential': round(goal_differential), 'Home Goals': home_goals, 'Away Goals': away_goals}
            elif goal_differential < 0:
                self.home.losses += 1
                self.away.wins += 1
                self.away.points += 2
                self.home.teams_lost_to.append(self.away)
                self.away.teams_beat.append(self.home)
                return {'Winner': self.away, 'Loser': self.home, 'Differential': round(goal_differential), 'Home Goals': home_goals, 'Away Goals': away_goals}

    def show_probabilities(self):
        if self.tie == True:
            home_win_probability = scipy.stats.norm.cdf((self.home.rating - self.away.rating - 0.5)/self.standard_deviation)
            tie_probability = scipy.stats.norm.cdf((self.home.rating - self.away.rating + 0.5)/self.standard_deviation) - scipy.stats.norm.cdf((self.home.rating - self.away.rating - 0.5)/self.standard_deviation)
            away_win_probability = scipy.stats.norm.cdf((self.away.rating - self.home.rating - 0.5)/self.standard_deviation)
            print('Home: ' + str(home_win_probability))
            print('Tie: ' + str(tie_probability))
            print('Away: ' + str(away_win_probability))
        elif self.tie == False:
            home_win_probability = scipy.stats.norm.cdf((self.home.rating - self.away.rating)/self.standard_deviation)
            away_win_probability = scipy.stats.norm.cdf((self.away.rating - self.home.rating)/self.standard_deviation)
            print('Home: ' + str(home_win_probability))
            print('Away: ' + str(away_win_probability))

def rank(teams_list):
    points_list = []
    ranked_list = []

    for team in teams_list:
        if team.points not in points_list:
            points_list.append(team.points)
    points_list.sort(reverse=True)

    points_dict = dict.fromkeys(points_list)

    for team in teams_list:
        try:
            points_dict[team.points].append(team)
        except:
            points_dict[team.points] = [team]

    for element in points_list:
        broken_tie_list = tiebreaker(points_dict[element])
        for team in range(len(broken_tie_list)):
            ranked_list.append(broken_tie_list[team])

    return ranked_list

def tiebreaker(tied_teams_list):
    ranked_list = []

    if len(tied_teams_list) == 1:
        ranked_list = tied_teams_list
    elif len(tied_teams_list) == 2:
        if tied_teams_list[1] in tied_teams_list[0].teams_beat:
            ranked_list = [tied_teams_list[0], tied_teams_list[1]]
        elif tied_teams_list[0] in tied_teams_list[1].teams_beat:
            ranked_list = [tied_teams_list[1], tied_teams_list[0]]
        else:
            if tied_teams_list[0].wins > tied_teams_list[1].wins:
                ranked_list = [tied_teams_list[0], tied_teams_list[1]]
            elif tied_teams_list[0].wins < tied_teams_list[1].wins:
                ranked_list = [tied_teams_list[1], tied_teams_list[0]]
            else:
                if tied_teams_list[0].goals_for/(tied_teams_list[0].goals_for + tied_teams_list[0].goals_against) > tied_teams_list[1].goals_for/(tied_teams_list[1].goals_for + tied_teams_list[1].goals_against):
                    ranked_list = [tied_teams_list[0], tied_teams_list[1]]
                else:
                    ranked_list = [tied_teams_list[1], tied_teams_list[0]]
    else:
        ranked_list = sorted(tied_teams_list, key=lambda team: (team.points, team.goals_for/(team.goals_for + team.goals_against)), reverse=True)

    return ranked_list

start = time.time()

simulations = 5000
print_each_season = False

all_time_group_1_stats = pd.DataFrame({'1st': [0,0,0,0], '2nd': [0,0,0,0], '3rd': [0,0,0,0], '4th': [0,0,0,0], 'Semi-Finals': [0,0,0,0], 'Finals': [0,0,0,0], 'Championship': [0,0,0,0]}, index=['Markham Waxers', 'Oakville Rangers Blue', 'Guelph Gryphons', 'Northumberland Nighthawks'], columns=['1st', '2nd', '3rd', '4th', 'Semi-Finals', 'Finals', 'Championship'])
all_time_group_2_stats = pd.DataFrame({'1st': [0,0,0,0], '2nd': [0,0,0,0], '3rd': [0,0,0,0], '4th': [0,0,0,0], 'Semi-Finals': [0,0,0,0], 'Finals': [0,0,0,0], 'Championship': [0,0,0,0]}, index=['Milton Winterhawks', 'Barrie Colts', 'Belle River Jr. Canadiens', 'Clarington Toros'], columns=['1st', '2nd', '3rd', '4th', 'Semi-Finals', 'Finals', 'Championship'])

for simulation in range(simulations):
    if print_each_season == True:
        print('SIMULATION ' + str(simulation+1))

    lakeshore_1 = Team('Northumberland Nighthawks', 91.19)
    tri_county_2 = Team('Oakville Rangers Blue', 93.00)
    tri_county_3 = Team('Guelph Gryphons', 92.18)
    york_simcoe_1 = Team('Markham Waxers', 93.52)
    bluewater = Team('Belle River Jr. Canadiens', 90.86)
    lakeshore_2 = Team('Clarington Toros', 90.53)
    tri_county_1 = Team('Milton Winterhawks', 93.26)
    york_simcoe_2 = Team('Barrie Colts', 93.06)

    group_1_list = [lakeshore_1, tri_county_2, tri_county_3, york_simcoe_1]
    group_2_list = [bluewater, lakeshore_2, tri_county_1, york_simcoe_2]
    teams_list = []
    teams_list.extend(group_1_list)
    teams_list.extend(group_2_list)

    game_1 = Game(york_simcoe_1, lakeshore_1, True)
    game_2 = Game(tri_county_3, tri_county_2, True)
    game_3 = Game(york_simcoe_2, lakeshore_2, True)
    game_4 = Game(bluewater, tri_county_1, True)
    game_5 = Game(tri_county_3, york_simcoe_1, True)
    game_6 = Game(lakeshore_1, tri_county_2, True)
    game_7 = Game(lakeshore_2, bluewater, True)
    game_8 = Game(tri_county_1, york_simcoe_2, True)
    game_9 = Game(tri_county_3, lakeshore_1, True)
    game_10 = Game(tri_county_2, york_simcoe_1, True)
    game_11 = Game(tri_county_1, lakeshore_2, True)
    game_12 = Game(bluewater, york_simcoe_2, True)

    # This section can be changed when the tournament starts, or if you would like to start the simulation from a certain moment within the tournament.
    # Set the game variable to None in order to be simulated, and input the dictionary if a game has already been played.
    # Examples:
    # result_1 = {'Winner': york_simcoe_1, 'Loser': lakeshore_1, 'Home Goals': 2, 'Away Goals': 1}
    # result_2 = {'Winner': None, 'Loser': None, 'Home Goals': 5, 'Away Goals': 5}
    # ^^ the result_2 dictionary would be the example of a game that ended in a tie
    
    result_1 = None
    result_2 = None
    result_3 = None
    result_4 = None
    result_5 = None
    result_6 = None
    result_7 = None
    result_8 = None
    result_9 = None
    result_10 = None
    result_11 = None
    result_12 = None

    games_list = [game_1, game_2, game_3, game_4, game_5, game_6, game_7, game_8, game_9, game_10, game_11, game_12]
    results_list = [result_1, result_2, result_3, result_4, result_5, result_6, result_7, result_8, result_9, result_10, result_11, result_12]

    scores = pd.DataFrame([], index=[1,2,3,4,5,6,7,8,9,10,11,12], columns=['Home Team', 'Score', 'Away Team', 'Simulated'])

    for game in range(len(games_list)):
        if results_list[game] == None:
            game_result = Game.simulate(games_list[game])
            scores.loc[game+1, 'Simulated'] = True
        else:
            game_result = results_list[game]
            games_list[game].home.goals_for += game_result['Home Goals']
            games_list[game].home.goals_against += game_result['Away Goals']
            games_list[game].away.goals_for += game_result['Away Goals']
            games_list[game].away.goals_against += game_result['Home Goals']
            if game_result['Winner'] == None and game_result['Loser'] == None:
                games_list[game].home.ties += 1
                games_list[game].away.ties += 1
                games_list[game].home.points += 1
                games_list[game].away.points += 1
                games_list[game].home.teams_tied.append(games_list[game].away)
                games_list[game].away.teams_tied.append(games_list[game].home)
            else:
                game_result['Winner'].wins += 1
                game_result['Loser'].losses += 1
                game_result['Winner'].points += 2
                game_result['Winner'].teams_beat.append(game_result['Loser'])
                game_result['Loser'].teams_lost_to.append(game_result['Winner'])
            scores.loc[game+1, 'Simulated'] = False

        scores.loc[game+1, 'Home Team'] = games_list[game].home.name
        scores.loc[game+1, 'Away Team'] = games_list[game].away.name
        scores.loc[game+1, 'Score'] = str(game_result['Home Goals']) + ' - ' + str(game_result['Away Goals'])

    if print_each_season == True:
        print(scores)

    standings_1 = pd.DataFrame([], index=[1,2,3,4], columns=['Team', 'Wins', 'Losses', 'Ties', 'Points', 'GF', 'GA', 'GF%'])

    for team in range(len(group_1_list)):
        standings_1.loc[team+1, 'Team'] = group_1_list[team].name
        standings_1.loc[team+1, 'Wins'] = group_1_list[team].wins
        standings_1.loc[team+1, 'Losses'] = group_1_list[team].losses
        standings_1.loc[team+1, 'Ties'] = group_1_list[team].ties
        standings_1.loc[team+1, 'Points'] = group_1_list[team].points
        standings_1.loc[team+1, 'GF'] = group_1_list[team].goals_for
        standings_1.loc[team+1, 'GA'] = group_1_list[team].goals_against
        try:
            standings_1.loc[team+1, 'GF%'] = round(group_1_list[team].goals_for/(group_1_list[team].goals_for + group_1_list[team].goals_against),3)
        except:
            standings_1.loc[team+1, 'GF%'] = 0.5

    standings_2 = pd.DataFrame([], index=[1,2,3,4], columns=['Team', 'Wins', 'Losses', 'Ties', 'Points', 'GF', 'GA', 'GF%'])

    for team in range(len(group_2_list)):
        standings_2.loc[team+1, 'Team'] = group_2_list[team].name
        standings_2.loc[team+1, 'Wins'] = group_2_list[team].wins
        standings_2.loc[team+1, 'Losses'] = group_2_list[team].losses
        standings_2.loc[team+1, 'Ties'] = group_2_list[team].ties
        standings_2.loc[team+1, 'Points'] = group_2_list[team].points
        standings_2.loc[team+1, 'GF'] = group_2_list[team].goals_for
        standings_2.loc[team+1, 'GA'] = group_2_list[team].goals_against
        try:
            standings_2.loc[team+1, 'GF%'] = round(group_2_list[team].goals_for/(group_2_list[team].goals_for + group_2_list[team].goals_against),3)
        except:
            standings_2.loc[team+1, 'GF%'] = 0.5
            
    if print_each_season == True:
        print('\nGROUP 1')
        print(standings_1)
        print('\nGROUP 2')
        print(standings_2)

        print()
    ranked_group_1 = rank(group_1_list)

    if print_each_season == True:
        print('1st: ' + ranked_group_1[0].name)
        print('2nd: ' + ranked_group_1[1].name)
        print('3rd: ' + ranked_group_1[2].name)
        print('4th: ' + ranked_group_1[3].name)
    all_time_group_1_stats.loc[ranked_group_1[0].name, '1st'] += 1
    all_time_group_1_stats.loc[ranked_group_1[1].name, '2nd'] += 1
    all_time_group_1_stats.loc[ranked_group_1[2].name, '3rd'] += 1
    all_time_group_1_stats.loc[ranked_group_1[3].name, '4th'] += 1
    all_time_group_1_stats.loc[ranked_group_1[0].name, 'Semi-Finals'] += 1
    all_time_group_1_stats.loc[ranked_group_1[1].name, 'Semi-Finals'] += 1

    if print_each_season == True:
        print()
    ranked_group_2 = rank(group_2_list)
    if print_each_season == True:
        print('1st: ' + ranked_group_2[0].name)
        print('2nd: ' + ranked_group_2[1].name)
        print('3rd: ' + ranked_group_2[2].name)
        print('4th: ' + ranked_group_2[3].name)
    all_time_group_2_stats.loc[ranked_group_2[0].name, '1st'] += 1
    all_time_group_2_stats.loc[ranked_group_2[1].name, '2nd'] += 1
    all_time_group_2_stats.loc[ranked_group_2[2].name, '3rd'] += 1
    all_time_group_2_stats.loc[ranked_group_2[3].name, '4th'] += 1
    all_time_group_2_stats.loc[ranked_group_2[0].name, 'Semi-Finals'] += 1
    all_time_group_2_stats.loc[ranked_group_2[1].name, 'Semi-Finals'] += 1

    semi_finals_1 = Game(ranked_group_1[0], ranked_group_2[1], False)
    semi_finals_2 = Game(ranked_group_2[0], ranked_group_1[1], False)

    semi_1_result = Game.simulate(semi_finals_1)
    semi_2_result = Game.simulate(semi_finals_2)

    if print_each_season == True:
        print()
        print(semi_finals_1.home.name + ' ' + str(semi_1_result['Home Goals']) + ' - ' + str(semi_1_result['Away Goals']) + ' ' + semi_finals_1.away.name + ' (Winner: ' + str(semi_1_result['Winner'].name) + ')')
        print(semi_finals_2.home.name + ' ' + str(semi_2_result['Home Goals']) + ' - ' + str(semi_2_result['Away Goals']) + ' ' + semi_finals_2.away.name + ' (Winner: ' + str(semi_2_result['Winner'].name) + ')')
    try:
        all_time_group_1_stats.loc[semi_1_result['Winner'].name, 'Finals'] += 1
    except:
        all_time_group_2_stats.loc[semi_1_result['Winner'].name, 'Finals'] += 1
    try:
        all_time_group_1_stats.loc[semi_2_result['Winner'].name, 'Finals'] += 1
    except:
        all_time_group_2_stats.loc[semi_2_result['Winner'].name, 'Finals'] += 1

    finals = Game(semi_1_result['Winner'], semi_2_result['Winner'], False)
    finals_result = Game.simulate(finals)

    if print_each_season == True:
        print()
        print(finals.home.name + ' ' + str(finals_result['Home Goals']) + ' - ' + str(finals_result['Away Goals']) + ' ' + finals.away.name + ' (Winner: ' + str(finals_result['Winner'].name) + ')')
    try:
        all_time_group_1_stats.loc[finals_result['Winner'].name, 'Championship'] += 1
    except:
        all_time_group_2_stats.loc[finals_result['Winner'].name, 'Championship'] += 1

    if print_each_season == True:
        print('----------------------------------------------------------------')

all_time_group_1_stats /= simulations*0.01
all_time_group_1_stats = round(all_time_group_1_stats,1)
all_time_group_2_stats /= simulations*0.01
all_time_group_2_stats = round(all_time_group_2_stats,1)

print()
print('GROUP 1')
print(all_time_group_1_stats)
print('\nGROUP 2')
print(all_time_group_2_stats)

end = time.time()
elapsed_time = end-start
print('\n' + str(simulations) + ' simulations in ' + str(round(elapsed_time,1)) + ' seconds.')
print('Simulation Speed: ' + str(round(simulations/elapsed_time)) + ' simulations per second.\n')
