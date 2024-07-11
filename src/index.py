# index.py

import env
import random
from common import Common
from player import Player
from skill_handler import skill_handler


class Main:

	def main():

		# メッセージ出力
		print()# 改行
		print("もじもん！ ©2024 mojimon Inc.")
		print(f"制限時間が {env.COUNT} 秒に設定されています。")

		# プレイヤー名入力
		print()# 改行
		playerA_name = input("▶ひとりめのプレイヤー名を入力してください。")
		playerB_name = input("▶ふたりめのプレイヤー名を入力してください。")

		# インスタンス生成
		playerA = Player(playerA_name, 0)
		playerB = Player(playerB_name, 0)

		# 継続区分
		continue_kbn = "1"
		# ゲーム回転数
		geme_index = 1
		# スキル処理結果
		skill_result = None

		# ゲームスタート
		while "1" == continue_kbn:

			# プレイヤー決定
			p1 = None
			p2 = None
			random_num = random.choice([1, 2])
			if 1 == random_num:
				p1 = playerA
				p2 = playerB
			else:
				p1 = playerB
				p2 = playerA

			print()# 改行
			# ラウンド数出力
			print(f"★  ROUND {geme_index} ★")
			# プレイヤー出力
			print(f"[ 先攻は{p1.name}さんです。]")

			# 名前入力
			print()# 改行
			player1_monster_name = input(f"▶{p1.name}さんのモンスター名を入力してください。")
			# 1Pモンスター生成
			player1_monster = Common.create_monster(player1_monster_name, p1, None)
			# ステータス評価
			player1_status_level = Common.status_level_judge(player1_monster)
			# 情報出力
			Common.print_status(player1_monster, player1_status_level)
			# 転生チャンス
			player1_monster = Common.rebirth(player1_monster, player1_status_level["total"])

			# 名前入力
			print()# 改行
			player2_monster_name = input(f"▶{p2.name}さんのモンスター名を入力してください。")
			# 2Pモンスター生成
			player2_monster = Common.create_monster(player2_monster_name, p2, None)
			# ステータス評価
			player2_status_level = Common.status_level_judge(player2_monster)
			# 情報出力
			Common.print_status(player2_monster, player2_status_level)
			# 転生チャンス
			player2_monster = Common.rebirth(player2_monster, player2_status_level["total"])

			# スキル処理（モンスター生成後（1P））
			skill_handler("created_monster", {"copy_monster": player1_monster, "copied_monster": player2_monster})
			# スキル処理（モンスター生成後（2P））
			skill_handler("created_monster", {"copy_monster": player2_monster, "copied_monster": player1_monster})

			# 決着フラグ
			finish_flg = False
			# バトル回転数
			battle_index = 1
			# 攻撃するモンスター
			_atk_monster = None
			# 守るモンスター
			_df_monster = None
			# 攻守スイッチフラグ
			atk_df_switch_flg = False
			# MVPワード
			mvp_word = "なし"
			# SS（サイレンスストック）
			silence_stock = 0

			# バトル
			while False == finish_flg:

				# 攻守判定

				# 攻守入れ替えなしの場合
				if False == atk_df_switch_flg:
					if 1 == battle_index % 2:
						_atk_monster = player1_monster
						_df_monster = player2_monster
					else:
						_atk_monster = player2_monster
						_df_monster = player1_monster
				# 攻守入れ替えありの場合
				else:
					if 1 == battle_index % 2:
						_atk_monster = player2_monster
						_df_monster = player1_monster
					else:
						_atk_monster = player1_monster
						_df_monster = player2_monster

				# スキル処理（攻守判定時）
				skill_result = skill_handler("judge_atk_or_df", {"atk_monster": _atk_monster, "df_monster": _df_monster})
				# 攻守更新
				atk_monster = skill_result["new_atk_monster"]
				df_monster = skill_result["new_df_monster"]
				# 攻守の入れ替えが発生していた場合
				if skill_result["message"] is not None:
					# 攻守スイッチフラグ更新
					if True == atk_df_switch_flg:
						atk_df_switch_flg = False
					else:
						atk_df_switch_flg = True
					# メッセージ出力
					print(skill_result["message"])

				# コメント表示
				print()# 改行
				# リーサルに必要な文字数を取得
				lethal_amount = Common.judge_lethal(atk_monster, df_monster, silence_stock)
				# リーサルが狙える場合
				if 0 < lethal_amount:
					# リーサルに必要な文字数を出力
					print(f"[ {lethal_amount} 文字以上の回答でリーサルです。]")
				# コメント出力
				input(f"▶{atk_monster.name}の攻撃です。（Enterでスタート）")

				# 最初の文字決定
				beginning_character = Common.random_character_create(1)
				# 最後の文字決定
				_final_character = Common.random_character_create(2)

				# スキル処理（文字決定後）
				final_character = skill_handler("decided_character", {"atk_monster": atk_monster, "final_character": _final_character})

				# 出題
				print(f"Q.「{beginning_character}」で始まり「{final_character}」で終わる")
				# カウントスタート
				Common.countdown(env.COUNT)

				# 回答受付
				answer = input(f"▶{atk_monster.player.name}さんは回答を入力してください。")
				# MVPワード更新
				if len(answer) > len(mvp_word):
					mvp_word = answer

				# 体力退避更新
				df_monster.escape_hp = df_monster.hp
				# 体力計算
				calculate_result = Common.hp_calculate(atk_monster, df_monster, len(answer), silence_stock)
				# SS更新
				silence_stock = calculate_result["silence_stock"]
				# 結果出力
				Common.print_result(atk_monster, df_monster, calculate_result)

				# 勝敗判定
				if 0 == df_monster.hp:
					# ループ終了
					finish_flg = True
					# 勝利数更新
					atk_monster.player.win += 1
					# 結果出力
					print()# 改行
					print(f"[ {atk_monster.player.name}さんの勝利！]")
					print(f"[ 最長の単語は「{mvp_word}」でした。]")
					print()# 改行
					print(f"[ {player1_monster.player.name}さんの勝利数：{player1_monster.player.win}（勝率{Common.calculate_win_rate(player1_monster.player.win, geme_index)}%）]")
					print(f"[ {player2_monster.player.name}さんの勝利数：{player2_monster.player.win}（勝率{Common.calculate_win_rate(player2_monster.player.win, geme_index)}%）]")
					# MVPワード更新
					mvp_word = "なし"

				# バトル回転数更新
				battle_index += 1

			# 継続確認
			print()# 改行
			continue_kbn = input("▶継続してあそびますか？ 1：はい 2：いいえ")

			# ゲーム回転数更新
			geme_index += 1


Main.main()