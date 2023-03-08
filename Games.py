from nba_api.live.nba.endpoints import boxscore, scoreboard

sb = scoreboard.ScoreBoard().get_dict()['scoreboard']
DATE = sb['gameDate']
GAMES = sb['games']

def getPlayerStats(player_id, game_id, side):
    player_bs = [player for player in boxscore.BoxScore(game_id=game_id).get_dict()['game'][side]['players'] if
                 player['personId'] == player_id]
    return player_bs


def getGameInfo(team):
    game_id = ''
    playing = False

    for game in GAMES:
        if game['homeTeam']['teamName'] == team:
            game_id = game['gameId']
            playing = True
        if game['awayTeam']['teamName'] == team:
            game_id = game['gameId']
            playing = True

    if not playing:
        return False

    return [game for game in GAMES if game['gameId'] == game_id][0]


def getSide(team):
    for game in GAMES:
        if game['homeTeam']['teamName'] == team:
            return 'homeTeam'
        if game['awayTeam']['teamName'] == team:
            return 'awayTeam'
