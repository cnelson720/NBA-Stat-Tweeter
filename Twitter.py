import tweepy


def send_twitter_update(api, api_secret, token, token_secret, status):
    auth = tweepy.OAuthHandler(api, api_secret)
    auth.set_access_token(token, token_secret)
    twitter = tweepy.API(auth)
    twitter.update_status(status=status)
