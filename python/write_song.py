import redis
import os
import json
import requests
from collections import defaultdict
import yaml

# Parameters
default_limit = 8
default_room = "mixed"
default_file = "test.yml"
default_log = "log.json"
verbose = 0

# Globals
song_id = 0
track_dict = defaultdict(int)
artist_log = {}

## Database meuk
# Replace default url and port when running in docker
if os.getenv("REDIS_URL"):
    db_url = os.getenv("REDIS_URL")
else:
    db_url = 'localhost'

if os.getenv("REDIS_PORT"):
    db_port = os.getenv("REDIS_PORT")
else:
    db_port = 6379
rc = redis.Redis(host=db_url, port=db_port, db=0)

# Clear db for debugging
if os.getenv("CLEAR_DB"):
    print('database will be cleared')
    rc.flushall()

if os.getenv("VERBOSE"):verbose = 2

# Functions
# Find the most frequest thing in a list
def most_frequent(List):
    return max(set(List), key = List.count)

def dump_log(data,logfile=default_log):
    json_dump = json.dumps(data, sort_keys=True, indent=4)
    f = open(logfile, "w")
    f.write(json_dump)
    f.close()

# Read the yaml file
def read_yml(inputfile=default_file):
    with open(inputfile, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            print("Loading complete")
        except yaml.YAMLError as exc:
            print(exc)

    return data

# Clean the name
def fix_name(name):
    name = name.replace(" ", "+")
    name = name.replace("&", "+")
    name = name.replace("%", "+")
    name = name.replace("\n", "")
    return name

def un_fix_name(name):
    name = name.replace("+", " ")
    name = name.replace("%20", " ")
    name = name.replace("\n", "")
    return name

# Get songs from API
def find_song_ids(artist,limit=default_limit,room=default_room):
    # oi oi marc
    global song_id
    global track_dict
    global artist_log
    # end oi oi
    url = "https://itunes.apple.com/search?term=" + artist + "&entity=song&limit=" + str(limit) + "&country=NL&sort=popular"
    rq = requests.get(url)

    # Raise error if statuscode not 200
    if rq.status_code != 200:
        print("Hit the rate limit, lets wait 10 sec")
        time.sleep(10)


    # Transform json input to python objects
    artist_latest = ""
    for counts in range(limit):
        try:
            json_lines = json.loads(rq.text)["results"][counts]
            artist_latest = str(json_lines["artistName"])

            rq_dict = {
              "song": str(json_lines["trackId"]),
              "artistName": str(json_lines["artistName"]),
              "trackName": str(json_lines["trackName"]),
              "trackViewUrl": str(json_lines["trackViewUrl"]),
              "previewUrl": str(json_lines["previewUrl"]),
              "artworkUrl60": str(json_lines["artworkUrl60"]),
              "artworkUrl100": str(json_lines["artworkUrl100"])
            }

            # Fill db with songs
            err = rc.hmset('song:'+str(song_id),rq_dict)
            if not(err):
                print("Error with " + str(json_lines["trackName"]))


            # Fill rooms with songs
            # deze database is echt hard gebeund door de bouwer van binb
            room_dict = {
                str(song_id): str(track_dict[room])
            }

            mixed_dict = {
                str(song_id): str(song_id)
            }

            err = rc.zadd(room,room_dict)
            if not (err):
                if err == 0 and verbose > 1:
                    print("Already in the room: " + str(json_lines["trackName"]))
                else:
                    print("Error with " + str(json_lines["trackName"]) + " in room: " + str(room))

            err = rc.zadd("mixed", mixed_dict)
            if not (err):
                if err == 0 and verbose > 1:
                    print("Already in the room: " + str(json_lines["trackName"]))
                else:
                    print("Error with " + str(json_lines["trackName"]) + " in room: " + str(room))

            # keep track of the song_id
            song_id += 1

            # Keep track of score and all the rooms
            track_dict[room] += 1
        except:
            break
    artist_log.update({artist_latest: un_fix_name(artist)})


data = read_yml("test.yml")
print ("All the rooms: ")
print(data.keys())

for room in data.keys():
    limit = data[room]["songs"]
    # print(limit)
    artists = data[room]["artists"]
    for artist in artists:
        # print(artist)
        find_song_ids(fix_name(artist),limit,room)

dump_log(artist_log)
