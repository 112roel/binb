import requests, re
from bs4 import BeautifulSoup
from csv import writer

folder = "output/"
maxLength = 30

genre = "seventies"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-70s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_={"artist-title"})

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()[3:]
    if(len(name) < maxLength):
        f.write(name)
        f.write("\n")

f.close()

print("\n"+ genre + " downloaded")

genre = "eighties"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-80s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="song-title")

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)

f.close()

print("\n"+ genre + " downloaded")

genre = "nineties"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-90s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll('a', attrs={'href' : re.compile('^https://www.amazon.com')})

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)
    f.write("\n")

f.close()

print("\n"+ genre + " downloaded")

genre = "zeroes"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-00s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll('a', attrs={'href' : re.compile('^https://www.amazon.com')})

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)
    f.write("\n")

f.close()

print("\n"+ genre + " downloaded")

genre = "tens"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-10s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="t40w-artist")

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)

f.close()

print("\n"+ genre + " downloaded")

genre = "sixties"

response = requests.get('https://top40weekly.com/top-100-artists-of-the-60s/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.findAll('a', attrs={'href' : re.compile('^https://www.amazon.com')})

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)
    f.write("\n")

f.close()

print("\n"+ genre + " downloaded")

genre = "nederlands"

response = requests.get('https://nederlandse-artiesten.startpagina.nl/')

soup = BeautifulSoup(response.text, 'html.parser')

artists = soup.find_all(class_="single-link")

f = open(folder + genre + ".txt", "w")

for artist in artists:
    name = artist.get_text()
    f.write(name)
    f.write("\n")

f.close()

print("\n"+ genre + " downloaded")