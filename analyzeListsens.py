# program that counts and prints the most listened to artists from lisntenbrainz api json
import json
from pprint import pprint
import operator
import pandas as pd
import matplotlib.pyplot as plt

with open('aahanaggarwal_lb-2018-10-22.json') as f:
    data = json.load(f)

artistsCount = {}

def checkSimilarName(artist): # checks artists names against common other spellings
    if artist == "a r rahman":
        return "ar rahman"
    elif artist == "k k":
        return "kk"
    elif artist == "ajay-atul":
        return "ajay - atul"
    elif artist == "":
        return "unknown"
    elif artist == "shankar-ehsaan-loy":
        return "shankar ehsaan loy"
    else:
        return artist

for listen in data: # go thru every track

    artists = listen['artist_name'].split(",") # split multi artists

    for i in range(len(artists)): # fix inconsistencies within each artist

        artists[i] = artists[i].lower() # set all chars to lower
        artists[i] = artists[i].replace(".", "") # remove dots after abbrvs
        artists[i] = checkSimilarName(artists[i])

        if "&" in artists[i]: # split artists with '&'
            temp = artists[i].split("&")
            artists.remove(artists[i])
            for a in temp:
                a = a.strip() # remove whitespace
                artists.append(a) # add back to array of artists

    for artist in artists:  # count artists
        if artist not in artistsCount: # set count for each artist
            artistsCount[artist] = 1
        else:
            artistsCount[artist] = artistsCount[artist] + 1

artists = list(artistsCount.keys())
values = list(artistsCount.values())

df = pd.DataFrame({'artists':artists, 'values':values})
df = df.sort_values(by=['values'], ascending=False)
df = df.head(10) # get top ten artists

plt.xlabel("Artists")
plt.ylabel("Count")
plt.xticks(rotation=90, fontSize=10)
plt.bar(df['artists'], df['values'])
plt.savefig('Top Ten Artists.png', bbox_inches='tight')