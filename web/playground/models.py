

class Season:
    def __init__(self, period, teams):
        self.period = period  # eg. 2008/2009
        self.teams = teams
        self.matches = list()


class Team:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Match:
    def __init__(self, day, home_team, away_team, home_team_points, away_team_points, home_team_odds, away_team_odds,
                 winner, playoffs, preseason):
        self.day = day  # eg. 27-03-2022
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_points = home_team_points
        self.away_team_points = away_team_points
        self.home_team_odds = home_team_odds
        self.away_team_odds = away_team_odds
        self.winner = winner
        self.playoffs = playoffs
        self.preseason = preseason

    def print_match(self):
        print(self.day, self.home_team, self.away_team, self.home_team_points, self.away_team_points,
              self.home_team_odds, self.away_team_odds, self.winner, self.playoffs, self.preseason)
