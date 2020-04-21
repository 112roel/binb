import requests
import re
from bs4 import BeautifulSoup
import yaml

output = {}

maxLength = 30
limit = 7

genre = "seventies"

output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-70s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_={"artist-title"})

for artist in artists:
    name = artist.get_text()[3:]
    if(len(name) < maxLength):
        output[genre]["artists"].append(name)

print("\n" + genre + " downloaded")

genre = "eighties"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-80s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="song-title")

for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))

print("\n" + genre + " downloaded")

genre = "nineties"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-90s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll(
    'a', attrs={'href': re.compile('^https://www.amazon.com')})


for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))

print("\n" + genre + " downloaded")

genre = "zeroes"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-00s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll(
    'a', attrs={'href': re.compile('^https://www.amazon.com')})


for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))

print("\n" + genre + " downloaded")

genre = "tens"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-10s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="t40w-artist")

for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))


print("\n" + genre + " downloaded")

genre = "sixties"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://top40weekly.com/top-100-artists-of-the-60s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll(
    'a', attrs={'href': re.compile('^https://www.amazon.com')})


for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))


print("\n" + genre + " downloaded")

genre = "nederlands"
output[genre] = {}
output[genre]["songs"] = limit
output[genre]["artists"] = []

response = requests.get('https://nederlandse-artiesten.startpagina.nl/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="single-link")


for artist in artists:
    name = artist.get_text()
    output[genre]["artists"].append(name.rstrip("\n"))


print("\n" + genre + " downloaded")

print("\nCreating output\n")

with open('output.yml', 'w') as file:
    documents = yaml.dump(output, file)
