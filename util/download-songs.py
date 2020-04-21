import requests
import json
import time

limit = 5

try:
    f = open("artist-ids.js", "r")
    artistIDS = []
    number = 0
    for line in f:
        if len(line) > 0:
            if any(char.isdigit() for char in line):
                artistId = line.split(" /")
                artistId = artistId[0].replace(',', '')
                artistId = artistId.strip()
                artistIDS.append(artistId)
                number = number + 1
    f.close()
except:
    print("error")

output = []
for artist_id in artistIDS:
    print("Dowloading: " + str(artist_id))
    url = "https://itunes.apple.com/lookup?id=" + \
        str(artist_id) + "&entity=song&limit=" + \
        str(limit) + "&country=NL&sort=popular"
    r = requests.get(url)

    if r.status_code != 200:
        print("Hit the rate limit, lets wait 10 sec")
        time.sleep(10)

    try:
        results = json.loads(r.text)["results"]
        print("Found: " + str(results[0]["artistName"]))
        output.append(results)
       
    except:
        print("error")


f = open("output.json", "w")
f.write(json.dumps(output))
f.close()
