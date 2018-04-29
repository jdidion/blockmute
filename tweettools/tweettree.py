#!/usr/bin/env python
# Fetch all
import sys
from tweettools import get_client

def walk_tweet_tree(tweet_id, fn=print):


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--tweet-id')
    parser.add_argument('-ck', '--consumer-key')
    parser.add_argument('-cs', '--consumer-secret')
    parser.add_argument('-tk', '--token-key', default=None)
    parser.add_argument('-ts', '--token-secret', default=None)
    parser.add_argument('-s', '--sleep-secs', type=int, default=15 * 60)
    args = parser.parse_args()

    api = get_client(args.token_key, args.token_secret, args.consumer_key, args.consumer_secret)
    walk_tweet_tree(api, args.tweet_id)

if __name__ == '__main__':
    main()