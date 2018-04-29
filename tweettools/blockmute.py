#!/usr/bin/env python
# Block everyone you've muted, and vice-versa.

from argparse import ArgumentParser
import time
from tqdm import tqdm
from tweettools import get_client

def blockmute(api, sleep_secs=300):
    mutes = set(api.GetMutesIDs())
    blocks = set(api.GetBlocksIDs())

    new_blocks =  mutes - blocks
    for user_id in tqdm(new_blocks):
        while True:
            try:
                api.CreateBlock(user_id)
                break
            except:
                print("Exceeded rate limit; sleeping for {} seconds".format(sleep_secs))
                time.sleep(sleep_secs)

    new_mutes = blocks - mutes
    for user_id in tqdm(new_mutes):
        while True:
            try:
                api.CreateMute(user_id)
                break
            except:
                print("Exceeded rate limit; sleeping for {} seconds".format(sleep_secs))
                time.sleep(sleep_secs)

def main():
    parser = ArgumentParser()
    parser.add_argument('-ck', '--consumer-key')
    parser.add_argument('-cs', '--consumer-secret')
    parser.add_argument('-tk', '--token-key', default=None)
    parser.add_argument('-ts', '--token-secret', default=None)
    parser.add_argument('-s', '--sleep-secs', type=int, default=15*60)
    args = parser.parse_args()

    api = get_client(args.token_key, args.token_secret, args.consumer_key, args.consumer_secret)
    blockmute(api, sleep_secs=args.sleep_secs)

if __name__ == '__main__':
    main()
