import itertools
import json
import pprint as pp
import requests

import nba_site_constants
import rating_loader

_DAYS_IN_WEEK = 7

class PlanFinder:

	def __init__(self):
		with open('dates.txt', 'r') as dates_file:
			day_list = dates_file.read().splitlines()
		self.week_list = list()
		for day in range(0, len(day_list), _DAYS_IN_WEEK):
			self.week_list.append(day_list[day:day + _DAYS_IN_WEEK])

		self.offensive_ratings = self._LoadJSONFile(nba_site_constants.
										OFFENSIVE_TEAM_RATINGS_FILE)
		self.defensive_ratings = self._LoadJSONFile(nba_site_constants.
										DEFENSIVE_TEAM_RATINGS_FILE)
		self.total_wins, self.total_losses = self._GetCurrentScore()
		self.team_to_id = nba_site_constants.TEAM_TO_ID_MAP
		self.id_to_team = nba_site_constants.ID_TO_TEAM_MAP

	def _FormScheduleUrl(self, date):
		return nba_site_constants.PROD_URL + date + '/scoreboard.json'

	def _UpdateOpponents(self, teams_opponents, hteam_id, vteam_id):
		if hteam_id in teams_opponents:
			teams_opponents[hteam_id].append(vteam_id)
		else:
			teams_opponents[hteam_id] = [vteam_id]
		if vteam_id in teams_opponents:
			teams_opponents[vteam_id].append(hteam_id)
		else:
			teams_opponents[vteam_id] = [hteam_id]		

	def _GetSchedule(self, date):
		url = self._FormScheduleUrl(date)
		response = requests.get(url)
		response.raise_for_status()
		teams_opponents = dict()
		for game in response.json()['games']:
			self._UpdateOpponents(teams_opponents, game['hTeam']['teamId'], game['vTeam']['teamId'])
		return teams_opponents

	def _ProbAWinsVsB(self, team, opponent):
		a_ortg = self.offensive_ratings[team]
		a_drtg = self.defensive_ratings[team]
		b_ortg = self.offensive_ratings[opponent]
		b_drtg = self.defensive_ratings[opponent]

		a_win_pct = a_ortg**16.5/(a_ortg**16.5 + a_drtg**16.5)
		b_win_pct = b_ortg**16.5/(b_ortg**16.5 + b_drtg**16.5)
		return a_win_pct * (1 - b_win_pct)/(a_win_pct * (1 - b_win_pct) + b_win_pct * (1 - a_win_pct))

	def _GetCurrentScore(self):
		total_wins = 0
		total_losses = 0
		for pick_info in nba_site_constants.PICKS.values():
			total_wins += pick_info['wins']
			total_losses += pick_info['losses']
		return total_wins, total_losses

	def _LoadJSONFile(self, file_name):
		with open(file_name) as file:
			data = json.load(file)
		return data

	def _TeamScoreForWeek(self, team_name, week, opponents):
		expected_wins = 0
		for opponent in opponents:
			opponent_name = self.id_to_team[opponent]
			expected_wins = expected_wins + self._ProbAWinsVsB(team_name, opponent_name)
		return expected_wins

	def _GetWeekSchedule(self, week):
		games_dict = dict()
		for day in self.week_list[week - 1]:
			for team, opponents in self._GetSchedule(day).items():
				if team in games_dict:
					games_dict[team].extend(opponents)
				else:
					games_dict[team] = opponents
		return games_dict


	def _GetNextWeek(self, week, picks):
		week_expectation = dict()
		schedule = self._GetWeekSchedule(week)
		pp.pprint(schedule)
		for team in nba_site_constants.TEAMS:
			if team in picks:
				continue
			print("evaluating team: ", team)
			opponents = schedule[self.team_to_id[team]]
			wins = self._TeamScoreForWeek(team, week, opponents)
			week_expectation[team] = {'wins': wins,
									  'losses': len(opponents) - wins}
		return week_expectation

	def _GetBestPlans(self, week, picks):
		week_expectation = _GetNextWeek(week, picks)
		total_games = total_wins + total_losses
		#compare = lambda (key, value): (value['wins'] + total_wins) / (total_games + value['wins'] + value['losses'])
		#sorted_week = sorted(week_expectation.iteritems(), key=compare, reverse=True)
		#if week < 24:
		#	return _BestPlan(_GetBestPlans(off_ratings, def_ratings, week + 1, total_wins))
		#else:
		#	return 


	def FindBestPlan(self):
		plans = self._GetBestPlans(nba_site_constants.WEEKS_PLAYED, 
								   nba_site_constants.PICKS.copy())

		return self._BestPlan(plans)



	def FormatPlan(self, plan):
		return sorted( ((value, key) for key, value in plan.items()), reverse=True)


def ComputeNextPick():
	rating_loader.LoadRatings()

if __name__ == "__main__":
	plan_finder = PlanFinder()
	pp.pprint(plan_finder._GetNextWeek(2, nba_site_constants.PICKS.copy()))
