import requests, time, json

#####
# Made by Marc
# This script uses the itunes api to find artist_ids by the names from the artistlist.txt
# It might no be perfect, but it works
# I'm not responsible for any damage done (lost friendships, etc)

# Parameters
search_limit = 10
rate_limit_sleep = 1
genre = "dbvh"

# Open artist file or use standard
try:
    f = open("artistlist.txt", "r")
    artist = []
    for line in f:
        line = line.replace(' ','+')
        line = line.replace('\n','')
        if len(line) > 0:artist.append(line)
    f.close()
    print("File loaded")
except:
    artist = ["cascada", "van halen", "iron maiden", "golden earring", "de dijk","go back to the zoo", "di-rect"]
    artist = [name.replace(' ', '+') for name in artist]

# Functions
def most_frequent(List):
    return max(set(List), key = List.count)

# print(artist)

artist_id_list = []
artist_name_list = []
for name in artist:
    print("Finding " + str(name))
    url = "https://itunes.apple.com/search?term=" + name + "&limit" + str(search_limit)
    r = requests.get(url)

    # Raise error if statuscode not 200
    if r.status_code != 200:
        print("Hit the rate limit, lets wait 10 sec")
        time.sleep(10)

    # Transform json input to python objects
    artist_ids = []
    for counts in range(search_limit):
        try:
            json_lines = json.loads(r.text)["results"][counts]
            artist_ids.append(json_lines["artistId"])
        except:
            break

    # If no artists is found, do not add anything
    # Otherwise, just take to most common artist
    if len(artist_ids) > 0:
        artist_id_list.append(most_frequent(artist_ids))
        artist_name_list.append(name.replace("+"," "))
    else:
        print(name + " cant be found")

    time.sleep(rate_limit_sleep)


# Write data to file
f = open("artist-ids.js", "w")
f.write("'use strict'; \n \nmodule.exports = {\n\t"+genre+": [\n")
for index, _ in enumerate(artist_id_list):
    f.write("\t\t" + str(artist_id_list[index]) + ", // " + artist_name_list[index] + "\n")
f.write("\t]\n};")
f.close()

print("\n Results:")
print(artist_id_list)

