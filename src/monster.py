# monster.py

class Monster:

	def __init__(self, name, hp, atk, df, skill, gyo, skill_used_flg, escape_hp, player):

		# 各種ステータス設定
		self.name = name
		self.hp = hp
		self.atk = atk
		self.df = df
		self.skill = skill
		self.gyo = gyo
		self.skill_used_flg = skill_used_flg
		self.escape_hp = escape_hp
		self.player = player