import csv

_CARMELO_PROB1 = 20
_CARMELO_PROB2 = 21

class FiveThirtyEightReader:

	_SEASON = '2019'

	def __init__(self):
		# Map of dates to list of game objects from 538. 
		self.date_to_elo = dict()
		self._Load538EloScores()

	def _Load538EloScores(self):
		"""Fills self.date_to_elo"""
		matched_row = None
		with open("538_stats/nba_elo.csv", "r") as elo_csv:
			reader = csv.reader(elo_csv, delimiter=',')
			for row in reader:
				if row[1] != self._SEASON:
					continue
				if row[0] in self.date_to_elo:
					self.date_to_elo[row[0]].append(row)
				else:
					self.date_to_elo[row[0]] = [row]

	def GetMap(self):
		return self.date_to_elo

