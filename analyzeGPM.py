import pandas as pd
import glob
from pprint import pprint
import matplotlib.pyplot as plt

# path = "C:\\Users\\aahan\\Desktop\\randomWork\\takeout-20181022T060548Z-001\\Takeout\\Google Play Music\\Tracks"
# filenames = glob.glob(path+ "/*.csv")

# frame = pd.DataFrame()
# list = []

# for filename in filenames:
#     df = pd.read_csv(filename, index_col=None, header=0, engine='python')
#     list.append(df)

# frame = pd.concat(list)

frame = pd.read_csv("allsongs.csv")

artistsCount = {}

for index, song in frame.iterrows():
    artists = str(song['Artist']).split(",")

    for i in range(len(artists)): # fix inconsistencies within each artist

        artists[i] = artists[i].lower() # set all chars to lower
        artists[i] = artists[i].replace(".", "") # remove dots after abbrvs

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
            artistsCount[artist] = artistsCount[artist] + song['Play Count']

artists = list(artistsCount.keys())
values = list(artistsCount.values())

df = pd.DataFrame({'artists':artists, 'values':values})
df = df.sort_values(by=['values'], ascending=False)
df = df.head(10) # get top ten artists

plt.xlabel("Artists", fontSize=20)
plt.ylabel("Count", fontSize=20)
plt.xticks(rotation=90, fontSize=12)
plt.bar(df['artists'], df['values'])
plt.savefig('Top Ten Artists GPM.png', bbox_inches='tight')
