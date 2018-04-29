from requests_oauthlib import OAuth1Session
import twitter as tw
import webbrowser

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

def get_client(consumer_key, consumer_secret, token_key=None, token_secret=None):
    if token_key is None or token_secret is None:
        token_key, token_secret = get_access_token(consumer_key, consumer_secret)

    return tw.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=token_key,
        access_token_secret=token_secret,
        sleep_on_rate_limit=True)

def get_access_token(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')
    resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    webbrowser.open(oauth_client.authorization_url(AUTHORIZATION_URL))
    pincode = input('\nEnter your pincode: ').strip()
    oauth_client = OAuth1Session(
        consumer_key, client_secret=consumer_secret, resource_owner_key=resp.get('oauth_token'),
        resource_owner_secret=resp.get('oauth_token_secret'), verifier=pincode)
    resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    return resp.get('oauth_token'), resp.get('oauth_token_secret')