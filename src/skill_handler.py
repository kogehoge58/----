# skill_handler.py

import random


def fantasista_function(monster):

	# 希望行確認
	print()# 改行
	print(f"[ {monster.name}は{monster.skill["name"]}です。]")
	gyo_wish = input(f"▶最後の文字に希望する行を入力してください。（例：あ行の場合→「あ」）")

	# 希望行設定
	monster.gyo = gyo_wish

def skill_handler(when, param):

	# ランダムな数字
	random_num = None

	# ステータス決定時
	if "decide_status" == when:

		# 更新予定のステータス
		new_hp = param["hp"]
		new_atk = param["atk"]
		new_df = param["df"]

		# 「大地の恵み」の場合
		if "004" == param["skill"]["code"]:
			new_hp = param["hp"] + 30
		# 「灼熱の怒り」の場合
		elif "005" == param["skill"]["code"]:
			new_atk = param["atk"] + 15
		# 「鋼の肉体」の場合
		elif "006" == param["skill"]["code"]:
			new_df = param["df"] + 10
		# その他の場合
		else:
			pass

		# ステータス返却
		return {"new_hp": new_hp, "new_atk": new_atk, "new_df": new_df}

	# 攻守判定時
	elif "judge_atk_or_df" == when:

		# 更新予定の攻守
		new_atk_monster = param["atk_monster"]
		new_df_monster = param["df_monster"]

		# メッセージ
		message = None

		# 防御側が「選ばれし者」だった場合
		if "003" == param["df_monster"].skill["code"]:
			# 1から10までのランダムな数字を生成
			random_num = random.randint(1, 10)

			# 10%の確率を当てた場合
			if 1 == random_num:

				# 攻守を入れ替える
				new_atk_monster = param["df_monster"]
				new_df_monster = param["atk_monster"]
				# メッセージ更新
				message = f"[ {new_atk_monster.name}は運命を捻じ曲げた！]"

		# 攻守返却
		return {"new_atk_monster": new_atk_monster, "new_df_monster": new_df_monster, "message": message}

	# モンスター生成後
	elif "created_monster" == when:

		# コピーする側が「パーフェクトトレース」だった場合
		if "007" == param["copy_monster"].skill["code"]:

			# 希望確認
			print()# 改行
			print(f"[ {param["copy_monster"].name}は{param["copy_monster"].skill["name"]}です。]")
			copy_wish = input(f"▶{param["copied_monster"].name}をコピーしますか？ 1：はい 2：いいえ")

			# コピーを希望した場合
			if "1" == copy_wish:

				# ステータスをコピーする
				param["copy_monster"].hp = param["copied_monster"].hp
				param["copy_monster"].atk = param["copied_monster"].atk
				param["copy_monster"].df = param["copied_monster"].df
				param["copy_monster"].skill = param["copied_monster"].skill
				# コメント出力
				print(f"[{param["copy_monster"].name}は{param["copied_monster"].name}に成り代わった！]")

				# コピー後のスキルが「ファンタジスタ」だった場合
				if "009" == param["copy_monster"].skill["code"]:
					# ファンタジスタ共通処理を実施
					fantasista_function(param["copy_monster"])

		# 処理対象が「ファンタジスタ」だった場合
		elif "009" == param["copy_monster"].skill["code"]:
			# ファンタジスタ共通処理を実施
			fantasista_function(param["copy_monster"])

	# 文字決定後
	elif "decided_character" == when:

		# 更新予定の最後の文字		
		new_final_character = param["final_character"]

		# 攻撃が「ファンタジスタ」だった場合
		if "009" == param["atk_monster"].skill["code"]:

			# 0から4までのランダムな数字を生成
			random_num = random.randint(0, 4)
			# 行格納用
			gyo_array = None

			# 希望行に応じた文字を設定
			if "あ" == param["atk_monster"].gyo:
				gyo_array = ["あ", "い", "う", "え", "お"]
				new_final_character = gyo_array[random_num]
			elif "か" == param["atk_monster"].gyo:
				gyo_array = ["か", "き", "く", "け", "こ"]
				new_final_character = gyo_array[random_num]
			elif "さ" == param["atk_monster"].gyo:
				gyo_array = ["さ", "し", "す", "せ", "そ"]
				new_final_character = gyo_array[random_num]
			elif "た" == param["atk_monster"].gyo:
				gyo_array = ["た", "ち", "つ", "て", "と"]
				new_final_character = gyo_array[random_num]
			elif "な" == param["atk_monster"].gyo:
				gyo_array = ["な", "に", "ぬ", "ね", "の"]
				new_final_character = gyo_array[random_num]
			elif "は" == param["atk_monster"].gyo:
				gyo_array = ["は", "ひ", "ふ", "へ", "ほ"]
				new_final_character = gyo_array[random_num]
			elif "ま" == param["atk_monster"].gyo:
				gyo_array = ["ま", "み", "む", "め", "も"]
				new_final_character = gyo_array[random_num]
			elif "や" == param["atk_monster"].gyo:
				random_num = random.randint(0, 2)
				gyo_array = ["や", "ゆ", "よ"]
				new_final_character = gyo_array[random_num]
			elif "ら" == param["atk_monster"].gyo:
				gyo_array = ["ら", "り", "る", "れ", "ろ"]
				new_final_character = gyo_array[random_num]
			else:
				random_num = random.randint(0, 1)
				gyo_array = ["わ", "ん"]
				new_final_character = gyo_array[random_num]

		# 最後の文字返却
		return new_final_character

	# ダメージ決定後
	elif "decided_damage" == when:

		# 更新予定のダメージ
		new_damage = param["damage"]

		# 攻撃が「龍の導き」だった場合
		if "002" == param["atk_monster"].skill["code"]:
			# 1から10までのランダムな数字を生成
			random_num = random.randint(1, 10)
			# 10%の確率を当てた場合
			if 1 == random_num:
				# ダメージ更新
				new_damage += 50
				# メッセージ出力
				print("[ 天空より龍が舞い降りた！]")

		# 防御が「天使の加護」だった場合
		if "001" == param["df_monster"].skill["code"]:
			# 1から10までのランダムな数字を生成
			random_num = random.randint(1, 10)
			# 10%の確率を当てた場合
			if 1 == random_num:
				# ダメージ更新
				new_damage = 0
				print("[ 天界より天使が舞い降りた！]")

		# ダメージ返却
		return new_damage

	# バトル結果出力時
	elif "print_battle_result" == when:

		# 防御の体力が0の場合
		if 0 == param["df_monster"].hp:
			# 防御が「不屈の精神」かつスキルを使用していない場合
			if "008" == param["df_monster"].skill["code"] and False == param["df_monster"].skill_used_flg:
				# 体力更新
				param["df_monster"].hp = 1
				# スキル使用フラグ更新
				param["df_monster"].skill_used_flg = True
				# コメント出力
				print(f"[ {param["df_monster"].name}は倒れない！]")

	else:
		pass