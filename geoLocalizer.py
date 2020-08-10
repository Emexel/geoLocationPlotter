# %% Geo Localization Plotter v1.1

import matplotlib
matplotlib.use('QT4Agg')
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mapFunctions import *

# %%
geolocator = Nominatim(user_agent="usrapp")

# locDic = {'City': ['Leonessa, PZ', 'Portopalo, SR', 'Messina, ME, IT', 'Barletta, BAT', 'Ischia, NA', 'San Fele, PZ', 'Caltavuturo, PA', 'Siracusa, SR', 'Santeramo in Colle, BA', 'Augusta, SR', 'Sava, TA', 'Torino, TO', 'Avigliano, PZ']}
locDic = {'City': ['Rome', 'Ushuaia', 'Attu Island, Alaska', ' Caroline Island, Kiribati']}
latitude = []
longitude = []

df = pd.DataFrame(locDic)

# %%
for city in df["City"]:
    loc = geolocator.geocode(city)
    if loc is not None:
        latitude.append(loc.latitude)
        longitude.append(loc.longitude)  


# %%
df["Latitude"] = latitude
df["Longitude"] = longitude

# df


# %%
midPt = [df["Latitude"].mean(), df["Longitude"].mean()]
#print(midPt)
#location = geolocator.reverse(midPt)
#print(location)


# %% 
fig,ax = plt.subplots()# plt.subplots(figsize=(8,8))
fig.tight_layout()


lats = df['Latitude'].to_numpy()
longs = df['Longitude'].to_numpy()

m = drawMap(lats, longs, 'l')

longM, latM = m(longs, lats)

# m.drawcounties()
# x, y = m(*zip(*[hawaii, austin, washington, chicago, losangeles]))



longMinVar, latMinVar = disvarmin(lats, longs)
xx, yy = m(longMinVar, latMinVar)
plt.plot(xx, yy, marker='*', markersize=14, color='r')
plt.text(xx, yy+2e4, 'Min. Dist.', color='r')

colors = cm.jet(np.linspace(0, 1, len(longM)))
labels = df['City'].to_numpy()

x,y = m(midPt[1], midPt[0])
plt.plot(x, y, 'rx', marker='*', markersize=14, color='k')
plt.text(x+1e4, y-3e4, 'Median')

for xpt, ypt, c, label in zip(longM, latM, colors, labels):
    plt.plot(xpt, ypt, marker='o', markersize=8, color=c)
    #circ = plt.Circle((xpt, ypt), np.sqrt((xpt - x)**2 + (ypt - y)**2), color=c, fill=False, lw=1.5)
    #ax.add_patch(circ)
    plt.text(xpt+00000, ypt-00000, label, fontsize=14)
       
#for xpt, ypt, c, label in zip(longM, latM, colors, labels):
        #circ2 = plt.Circle((xpt, ypt), np.sqrt((xpt - xx)**2 + (ypt - yy)**2), color=c, fill=False, lw=1.5, ls='--')
        #ax.add_patch(circ2)

#plt.plot(midLatM, midLongM, marker='*', markersize=14, color='k')
#plt.plot(longMinVarM, latMinVarM, marker='*', markersize=14, color='r')
#plt.text(midLongM+1e4, midLatM-7e4, 'Median')
#plt.text(latMinVarM+1e4, latMinVarM, 'Min. Dist.')
#plt.title('Mercator Projection')
saveFig = False
if saveFig:
    plt.savefig('mappa', bbox_inches='tight')

# plt.switch_backend('Qt4Agg')

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
plt.rcParams.update({'font.size': 16})





