import boto3
import json
import os
import pydash
import tweepy

TMP_FILE = '/tmp/data.json'


def setTwitterAuth():
    """
    obtains authorization from twitter API
    """
    # sets the auth tokens for twitter using tweepy
    auth = tweepy.OAuthHandler(
        os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'),
                          os.getenv('ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    return api


def getDataFromS3(fname):
    """
    downloads song data from S3
    """
    s3 = boto3.resource('s3')
    s3.Object('song-of-the-day', 'data.json').download_file(fname)


def putDataInS3(fname):
    """
    saves song data in S3
    """
    s3 = boto3.resource('s3')
    s3.Object('song-of-the-day', 'data.json').upload_file(fname)


def chooseSong(song_data):
    """
    chooses a song to tweet and updates recently choosen songs
    """
    recent = song_data['recentSongIds']
    songs = song_data['songs']

    # filter out recently choosen songs and randomly choose a song
    filtered_song_ids = pydash.filter_(songs.keys(), lambda x: x not in recent)
    song_id = pydash.sample(filtered_song_ids)

    # get chosen song and increment play count
    song = songs[song_id]
    song['playCount'] += 1

    # pop least recently choosen song and push new one
    if len(recent) == 7:
        pydash.shift(recent)
    pydash.push(recent, song_id)

    return song


def postTweet(tw, song):
    tweet = '{artist} - {name} {url} #SongOfTheDay'.format_map(song)
    if len(song['hashtags']) > 0:
        tweet += ' ' + song['hashtags'].join(' ')
    if song['handle'] != '':
        tweet += ' ' + song['handle']
    print('Sending tweet:\n' + tweet)
    tw.update_status(tweet, auto_populate_reply_metadata=True)


def lambda_handler(event, context):
    tw = setTwitterAuth()
    user = tw.me()
    print('Authenticated as ' + user.screen_name)

    getDataFromS3(TMP_FILE)
    print('Downloaded file from S3')

    with open('/tmp/data.json', 'r', encoding='utf-8') as f:
        song_data = json.load(f)
        song = chooseSong(song_data)
        postTweet(tw, song)

    with open('/tmp/data.json', 'w', encoding='utf-8') as f:
        json.dump(song_data, f, indent=2)

    putDataInS3(TMP_FILE)
    print('Saved file to S3')
