import boto3
import json
import os
import sys

class Done(Exception): pass

def getDataFromS3():
  s3 = boto3.resource('s3')
  s3.Object('song-of-the-day', 'data.json').download_file('/tmp/data.json')

def putDataInS3():
  s3 = boto3.resource('s3')
  s3.Object('song-of-the-day', 'data.json').upload_file('/tmp/data.json')

def loadJSON(fname):
  try:
    with open(fname, 'r', encoding='utf-8') as f:
      return json.load(f)
  except OSError:
    print('error reading file')
    sys.exit(1)

def saveJSON(data, fname):
  try:
    with open(fname, 'w', encoding='utf-8') as f:
      json.dump(data, f, indent=2)
  except OSError:
    print('error writing file')
    sys.exit(1)

def getInput(prompt):
  value = input(prompt)
  if value.strip().lower() == 'exit':
    raise Done
  return value

def addSong(data, id, name, artist, handle, url, hashtags):
  if hashtags != '':
    hashtags = [tag.strip() for tag in hashtags.split(',')]
  else:
    hashtags = []

  song = {
    'artist': artist,
    'handle': '@' + handle,
    'name': name,
    'url': url,
    'hashtags': hashtags,
    'playCount': 0
  }
  data['songs'][id] = song

if __name__ == '__main__':
  getDataFromS3()
  data = loadJSON('/tmp/data.json')
  print("Successfully loaded!")

  modified = False
  id = int(max(data['songs'].keys())) + 1

  try:
    while True:
      name = getInput("Enter song name (or 'exit' to quit): ")
      artist = getInput("Enter artist: ")
      handle = getInput("Enter artist handle: ")
      url = getInput("Enter URL: ")
      hashtags = getInput("Enter hashtags, comma separated: ")
      addSong(data, id, name, artist, handle, url, hashtags)
      modified = True
      id += 1
  except Done:
    pass

  if modified:
    saveJSON(data, '/tmp/data.json')
    putDataInS3()
    print("Successfully saved!")
