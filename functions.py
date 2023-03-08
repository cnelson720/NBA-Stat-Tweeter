import dateutil.parser as dp
from dateutil import tz
from datetime import datetime


class Percent(float):
    def __str__(self):
        return '{:.0%}'.format(self)


def is_playing(_player):
    if _player['status'] == 'INACTIVE':
        return False
    else:
        return True


def get_time_until_game(gameTime, currentTime):
    # '2023-03-05T016:00:00Z'
    parse_game_time = (dp.parse(gameTime))
    time_until_seconds = parse_game_time.timestamp()

    """temp_current = dp.parse(currentTime)
    temp_current_seconds = temp_current.timestamp()"""

    return time_until_seconds - currentTime


def convert_to_denver_time(gameTime):
    # "2023-03-09T02:00:00Z" example of gameTime
    parsed_time = dp.parse(gameTime)
    time_string_utc = str(parsed_time)[:19]
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Denver')
    utc = datetime.strptime(time_string_utc, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    mtn = utc.astimezone(to_zone).time().strftime("%I:%M %p")
    return mtn
