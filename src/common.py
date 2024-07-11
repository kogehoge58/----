# common.py

import env
import time
import math
import random
import skills
from monster import Monster
from skill_handler import skill_handler


class Common:

	def rebirth(monster, total):

		# 総合評価C以下の場合
		if 260 >= total:

			# メッセージ出力
			print()# 改行
			print(f"[ {monster.name}は転生できる可能性があります。]")
			print(f"[ 注：転生チャレンジに 3 文字以上の回答で転生が可能となります。]")
			print(f"[ 注：一度転生すると元のステータスには戻せません。]")
			print(f"[ 注：転生後の各ステータス最大値は通常生成時より低くなります。]")
			print(f"[ 注：転生後は転生前のスキルが受け継がれます。]")

			# 意思確認
			print()# 改行
			wish = input(f"▶転生チャレンジに挑戦しますか？ 1：はい 2：いいえ")

			# 転生チャレンジ
			if "1" == wish:

				# 開始合図
				input(f"▶Enterで転生チャレンジをスタートします。")
				# 最初の文字決定
				beginning_character = Common.random_character_create(1)
				# 最後の文字決定
				final_character = Common.random_character_create(2)
				# 出題
				print(f"Q.「{beginning_character}」で始まり「{final_character}」で終わる")
				# カウントスタート
				Common.countdown(env.COUNT)
				# 回答受付
				answer = input(f"▶回答を入力してください。")

				# チャレンジ成功
				if 3 <= len(answer):

					print()# 改行
					# コメント出力
					print(f"[ {monster.name}は生まれ変わった！]")
					# 再生成
					new_monster = Common.create_monster("Re:" + monster.name, monster.player, monster.skill)
					# ステータス評価
					new_status_level = Common.status_level_judge(new_monster)
					# 情報出力
					Common.print_status(new_monster, new_status_level)
					# インスタンス返却
					return new_monster

				else:

					print()# 改行
					# コメント出力
					print(f"[ {monster.name}は変われなかった、、、。]")
					# インスタンス返却
					return monster

			else:
				# インスタンス返却
				return monster

		else:
			# インスタンス返却
			return monster

	def judge_lethal(atk_monster, df_monster, silence_stock):

		def judge(magni):
			# 威力計算（小数点切り捨て）
			atk_amount = math.floor(atk_monster.atk * magni + silence_stock)
			# ダメージ計算
			damage = atk_amount - df_monster.df
			# ダメージは最低で0
			if 0 > damage:
				damage = 0
			# 判定返却
			return 0 >= df_monster.hp - damage

		# 必要文字数
		num = 0

		# リーサル判定
		if True == judge(1.0):
			num = 3
		elif True == judge(1.2):
			num = 4
		elif True == judge(1.4):
			num = 5
		elif True == judge(1.6):
			num = 6
		elif True == judge(1.8):
			num = 7
		elif True == judge(2.0):
			num = 8
		else:
			pass

		# 必要文字数返却
		return num

	def random_decide_skill():

		# 0から9までのランダムな数字を生成
		num = random.randint(0, 9)
		# num = random.choice([0, 1])
		# スキル決定を決定し返却
		# return skills.SKILLS[3]
		return skills.SKILLS[num]

	def calculate_win_rate(win, matches):

		return math.floor(win / matches * 100)

	def print_result(atk_monster, df_monster, result):

		# 攻撃を行った場合
		if True == result["damage_flg"]:

			# 結果出力
			print(f"[ {atk_monster.name}の攻撃！({atk_monster.atk} × {result["magnification"]}) ]")
			# ダメージが0の場合
			if 0 == result["damage"]:
				print(f"[ しかし{df_monster.name}にダメージはない！]")
			else:
				print(f"[ {df_monster.name}は {result["damage"]} のダメージを受けた！]")

		else:

			# 結果出力
			print(f"[ {atk_monster.name}の攻撃！]")
			print(f"[ しかし{atk_monster.name}は外してしまった！]")

		# スキル処理（バトル結果出力時）
		skill_handler("print_battle_result", {"df_monster": df_monster})
		# 体力出力
		print(f"[ {df_monster.name}の体力残り：{df_monster.escape_hp} -> {df_monster.hp} ]")

		# SS出力
		if 0 < result["silence_stock"]:
			print()# 改行
			print(f"[ SS（サイレンスストック）：{result["silence_stock"]} ]")

	def hp_calculate(atk_monster, df_monster, answer_amount, silence_stock):

		# 倍率決定
		if 2 >= answer_amount:
			magnification = 0
		elif 3 == answer_amount:
			magnification = 1.0
		elif 4 == answer_amount:
			magnification = 1.2
		elif 5 == answer_amount:
			magnification = 1.4
		elif 6 == answer_amount:
			magnification = 1.6
		elif 7 == answer_amount:
			magnification = 1.8
		else:
			magnification = 2.0

		# ダメージフラグ
		damage_flg = True
		# 威力
		atk_amount = None
		# ダメージ
		damage = None
		# 更新予定のSS
		new_silence_stock = silence_stock

		# 回答なしの場合
		if 0 == magnification:
			# ダメージフラグ更新
			damage_flg = False
			# SS更新
			new_silence_stock = silence_stock + 10
		else:
			# メッセージ出力
			if 0 < new_silence_stock:
				print(f"[ {atk_monster.name}が沈黙を破る！]")
			# 威力計算（小数点切り捨て）
			atk_amount = math.floor(atk_monster.atk * magnification + new_silence_stock)
			# ダメージ決定
			_damage = atk_amount - df_monster.df
			# ダメージは最低で0
			if 0 > _damage:
				_damage = 0
			# スキル処理（ダメージ決定後）
			damage = skill_handler("decided_damage", {"damage": _damage, "atk_monster": atk_monster, "df_monster": df_monster})
			# HP更新
			df_monster.hp -= damage
			# 体力は0が最低値
			if 0 > df_monster.hp:
				df_monster.hp = 0
			# SS更新
			new_silence_stock = 0

		# レスポンス返却
		return {"magnification": magnification, "damage": damage, "damage_flg": damage_flg, "df_monster": df_monster, "silence_stock": new_silence_stock}

	def countdown(seconds):

		while seconds:
			# 制限時間出力
			print(f"！制限時間残り：{seconds}秒", end="\r")
			# カウント
			time.sleep(1)
			# 出力時間更新
			seconds -= 1

	def random_character_create(character_kbn):

		# 文字の配列
		character_array = [
			"あ", "い", "う", "え", "お",
			"か", "き", "く", "け", "こ",
			"さ", "し", "す", "せ", "そ",
			"た", "ち", "つ", "て", "と",
			"な", "に", "ぬ", "ね", "の",
			"は", "ひ", "ふ", "へ", "ほ",
			"ま", "み", "む", "め", "も",
			"や", "ゆ", "よ",
			"ら", "り", "る", "れ", "ろ",
			"わ", "ん"
		]

		# 0から44までの数字をランダムで選定
		random_num = random.randint(0, 44)
		# 文字決定
		character = character_array[random_num]
		# 最初の文字の場合
		if 1 == character_kbn:
			# 「ん」の場合はもう一度
			while "ん" == character:
				random_num = random.randint(0, 44)
				character = character_array[random_num]

		# 文字返却
		return character

	def print_status(monster, level):

		# ステータス出力
		print(f"【{monster.name}のステータス】")
		print(f"・HP：{str(monster.hp)}{level["hp_level"]}")
		print(f"・攻撃：{str(monster.atk)}{level["atk_level"]}")
		print(f"・防御：{str(monster.df)}{level["df_level"]}")
		print(f"・合計：{str(level["total"])}/350")
		print(f"・{level["total_level"]}")
		print(f"・スキル名：{monster.skill["name"]}")
		print(f"・スキル説明：{monster.skill["description"]}")

	def status_level_judge(monster):

		# 評価結果
		hp_level = None
		atk_level = None
		df_level = None

		# HP評価
		if 160 >= monster.hp:
			hp_level = "( ★ ☆ ☆ ☆ ☆ )"
		elif 170 >= monster.hp:
			hp_level = "( ★ ★ ☆ ☆ ☆ )"
		elif 180 >= monster.hp:
			hp_level = "( ★ ★ ★ ☆ ☆ )"
		elif 190 >= monster.hp:
			hp_level = "( ★ ★ ★ ★ ☆ )"
		elif 200 >= monster.hp:
			hp_level = "( ★ ★ ★ ★ ★ )"
		else:
			hp_level = "( B R E A K )"

		# 攻撃評価
		if 60 >= monster.atk:
			atk_level = "( ★ ☆ ☆ ☆ ☆ )"
		elif 70 >= monster.atk:
			atk_level = "( ★ ★ ☆ ☆ ☆ )"
		elif 80 >= monster.atk:
			atk_level = "( ★ ★ ★ ☆ ☆ )"
		elif 90 >= monster.atk:
			atk_level = "( ★ ★ ★ ★ ☆ )"
		elif 100 >= monster.atk:
			atk_level = "( ★ ★ ★ ★ ★ )"
		else:
			atk_level = "( B R E A K )"

		# 防御評価
		if 10 >= monster.df:
			df_level = "( ★ ☆ ☆ ☆ ☆ )"
		elif 20 >= monster.df:
			df_level = "( ★ ★ ☆ ☆ ☆ )"
		elif 30 >= monster.df:
			df_level = "( ★ ★ ★ ☆ ☆ )"
		elif 40 >= monster.df:
			df_level = "( ★ ★ ★ ★ ☆ )"
		elif 50 >= monster.df:
			df_level = "( ★ ★ ★ ★ ★ )"
		else:
			df_level = "( B R E A K )"

		# 総合評価
		total = monster.hp + monster.atk + monster.df
		if 230 >= total:
			total_level = "総合評価...D"
		elif 260 >= total:
			total_level = "総合評価...C"
		elif 290 >= total:
			total_level = "総合評価...B"
		elif 320 >= total:
			total_level = "総合評価...A"
		else:
			total_level = "総合評価...S"

		# レスポンス返却
		return {
			"hp_level": hp_level,
			"atk_level": atk_level,
			"df_level": df_level,
			"total": total,
			"total_level": total_level
		}

	def create_monster(name, player, param_skill):

		# 一時ステータス
		_hp = None
		_atk = None
		_df = None
		# ステータス
		hp = None
		atk = None
		df = None
		# スキル
		skill = None
		# 希望行
		gyo = None
		# スキル使用フラグ
		skill_used_flg = False

		# 通常生成
		if param_skill is None:

			# HPをランダムで決定
			_hp = random.randint(150, 200)
			# 攻撃をランダムで決定
			_atk = random.randint(50, 100)
			# 防御をランダムで決定
			_df = random.randint(0, 50)
			# スキルをランダムで決定
			skill = Common.random_decide_skill()

		# 転生生成
		else:

			# HPをランダムで決定
			_hp = random.randint(150, 190)
			# 攻撃をランダムで決定
			_atk = random.randint(50, 90)
			# 防御をランダムで決定
			_df = random.randint(0, 40)
			# スキルを引き継ぐ
			skill = param_skill

		# スキル処理（ステータス決定時）
		skill_result = skill_handler("decide_status", {"hp": _hp, "atk": _atk, "df": _df, "skill": skill})
		# ステータス更新
		hp = skill_result["new_hp"]
		atk = skill_result["new_atk"]
		df = skill_result["new_df"]
		# 体力退避
		escape_hp = hp

		# インスタンス返却
		return Monster(name, hp, atk, df, skill, gyo, skill_used_flg, escape_hp, player)