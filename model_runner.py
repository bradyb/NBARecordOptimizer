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
		self.week_schedules = dict()
		self.team_week_score = dict()

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
		init_team = True
		if team_name in self.team_week_score:
			if week in self.team_week_score[team_name]:
				return self.team_week_score[team_name][week]
			init_team = False

		if init_team:
			self.team_week_score[team_name] = dict()
		expected_wins = 0
		for opponent in opponents:
			opponent_name = self.id_to_team[opponent]
			expected_wins = expected_wins + self._ProbAWinsVsB(team_name, opponent_name)
		return expected_wins

	def _GetWeekSchedule(self, week):
		if week in self.week_schedules:
			return self.week_schedules[week]

		games_dict = dict()
		for day in self.week_list[week - 1]:
			for team, opponents in self._GetSchedule(day).items():
				if team in games_dict:
					games_dict[team].extend(opponents)
				else:
					games_dict[team] = opponents
		self.week_schedules[week] = games_dict
		return games_dict


	def _GetNextWeek(self, week, picks):
		week_expectation = dict()
		schedule = self._GetWeekSchedule(week)
		for team in nba_site_constants.TEAMS:
			if team in picks:
				continue
			opponents = schedule[self.team_to_id[team]]
			wins = self._TeamScoreForWeek(team, week, opponents)
			week_expectation[team] = {'wins': wins,
									  'losses': len(opponents) - wins}
		return week_expectation

	def _GetBestPlans(self, week, picks):
		print("Week: ", week)
		week_expectation = self._GetNextWeek(week, picks)
		total_games = self.total_wins + self.total_losses

		value_dict = dict() 
		for team, scores in week_expectation.items():
			week_value = (scores['wins'] + self.total_wins) / (total_games + scores['wins'] + scores['losses'])
			value_dict[team] = week_value

		sorted_week = sorted(value_dict.items(), key=lambda kv: kv[1], reverse=True)
		if week < 24:
			top_plans = list()
			for next_week in range(min(3, 24 - week)):
				updated_picks = picks.copy()
				next_team = sorted_week[next_week][0]
				updated_picks[next_team] = {'week': week, 
											'wins': week_expectation[next_team]['wins'],
											'losses': week_expectation[next_team]['losses']}
				print("Week: ", week)
				print("Version: ", next_week)
				top_plans.append(self._GetBestPlans(week + 1, updated_picks))
			return self._BestPlan(top_plans)
		else:
			print("Reached base case, picking: ", sorted_week[0][0])
			updated_picks = picks.copy()
			next_team = sorted_week[0][0]
			updated_picks[next_team] = {'week': week, 
										'wins': week_expectation[next_team]['wins'],
										'losses': week_expectation[next_team]['losses']}
			return updated_picks

	def _BestPlan(self, picks_list):
		best_score = 0
		best_plan = None
		for picks in picks_list:
			score = self._ComputePlanScore(picks)

			if score > best_score:
				best_score = score
				best_plan = picks

		return best_plan

	def _ComputePlanScore(self, plan):
		total_wins = 0
		total_games = 0
		for scores in plan.values():
			total_wins += scores['wins']
			total_games += scores['wins'] + scores['losses']

		return (total_wins / total_games)

	def FindBestPlan(self):
		plans = self._GetBestPlans(nba_site_constants.WEEKS_PLAYED + 1, 
								   nba_site_constants.PICKS.copy())

		return plans



	def FormatPlan(self, plan):
		return sorted( ((value, key) for key, value in plan.items()), reverse=True)


def ComputeNextPick():
	rating_loader.LoadRatings()

if __name__ == "__main__":
	plan_finder = PlanFinder()
	best_plan = plan_finder.FindBestPlan() 
	pp.pprint(best_plan)
	print("Plan score: ", plan_finder._ComputePlanScore(best_plan))
