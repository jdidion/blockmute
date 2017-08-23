#!/usr/bin/env python

from argparse import ArgumentParser
from requests_oauthlib import OAuth1Session
import time
from tqdm import tqdm
import twitter as tw
import webbrowser

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

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

def blockmute(api):
    mutes = set(api.GetMutesIDs())
    blocks = set(api.GetBlocksIDs())

    new_blocks =  mutes - blocks
    for user_id in tqdm(new_blocks):
        while True:
            try:
                api.CreateBlock(user_id)
                break
            except:
                print("Exceeded rate limit; sleeping for 15 minutes")
                time.sleep(15*60)

    new_mutes = blocks - mutes
    for user_id in tqdm(new_mutes):
        while True:
            try:
                api.CreateMute(user_id)
                break
            except:
                print("Exceeded rate limit; sleeping for 15 minutes")
                time.sleep(15*60)

def main():
    parser = ArgumentParser()
    parser.add_argument('-ck', '--consumer-key')
    parser.add_argument('-cs', '--consumer-secret')
    parser.add_argument('-tk', '--token-key', default=None)
    parser.add_argument('-ts', '--token-secret', default=None)
    args = parser.parse_args()

    token_key = args.token_key
    token_secret = args.token_secret
    if token_key is None or token_secret is None:
        token_key, token_secret = get_access_token(args.consumer_key, args.consumer_secret)

    api = tw.Api(
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret,
        access_token_key=token_key,
        access_token_secret=token_secret,
        sleep_on_rate_limit=True)

    blockmute(api)

if __name__ == '__main__':
    main()
