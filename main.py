#!/usr/bin/python
import json
import sys
import time
import logging
from datetime import datetime
from Config import keys, player
from Games import getPlayerStats, getGameInfo, getSide
from Twitter import send_twitter_update
from functions import Percent, is_playing, get_time_until_game, convert_to_denver_time

# get TD record json data
with open('TD_Tracker.json') as f:
    current_td_count = json.load(f)

# get desired player from config
TEAM_NAME = player['team']
PLAYER_NAME = player['name']
PLAYER_ID = player['player_id']
TD = False

# find out if away or home. This is necessary for parsing team data.
SIDE = getSide(player['team'])

# get game info like start time and game status. 1 = not started 2 = started 3 = finished
game_info = getGameInfo(TEAM_NAME)

logging.basicConfig(filename='nba.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

if not game_info:
    logging.info(f"{TEAM_NAME} aren't playing today.")
    sys.exit()

game_id = game_info['gameId']

# sleep until the game begins
time_to_sleep = get_time_until_game(game_info['gameTimeUTC'], datetime.now().timestamp())

if time_to_sleep > 0:
    logging.info(f"{game_info['homeTeam']['teamName']} vs {game_info['awayTeam']['teamName']}. Sleeping until game begins at {convert_to_denver_time(game_info['gameTimeUTC'])}")
    time.sleep(time_to_sleep)

try:
    player_info = getPlayerStats(PLAYER_ID, game_id, SIDE)
    if not is_playing(player_info):
        logging.info(f"{PLAYER_NAME} won't be playing today.")
        sys.exit()
except Exception as e:
    logging.error(f"{e} / Game may not have started yet.")

while game_info['gameStatus'] == 2:
    time.sleep(60)
    player_stats = player['statistics']
    points, assists, rebounds = [player_stats[stat] for stat in ('points', 'assists', 'reboundsTotal')]
    minutes = f"{player_stats['minutes'][2:4]}:{player_stats['minutes'][5:7]}"
    fg_perc = Percent(player_stats['fieldGoalsPercentage'])

    if points >= 10 and assists >= 10 and rebounds >= 10:
        # triple double
        current_td_count['triple_doubles'] += 1
        status = f"Triple double #{current_td_count['triple_doubles']} for Jokic! {points} points, " \
                 f"{assists} rebounds, {rebounds} assists with {fg_perc} FG in {minutes} minutes.\n\n{current_td_count['record'] - current_td_count['triple_doubles']} " \
                 f"triple doubles left to beat the record"
        send_twitter_update(keys['TWITTER_API'], keys['TWITTER_SECRET'], keys['TOKEN'], keys['TOKEN_SECRET'],
                            status=status)
        logging.info(f"{PLAYER_NAME} had a triple double! Tweet sent at {datetime.now()}")
        TD = True
        break

    player_info = getPlayerStats(PLAYER_ID, TEAM_NAME, SIDE)
    game_info = getGameInfo(TEAM_NAME)

if TD:
    logging.info(f"{PLAYER_NAME} had a triple double and the game has finished.")
else:
    logging.info(f"Game finished with no triple double.")

with open('/Users/chrisnelson/Documents/PycharmProjects/nba/TD_Tracker.json', 'w') as f:
    json.dump(current_td_count, f)
