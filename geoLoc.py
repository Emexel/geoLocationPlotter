# %%
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from disvarmin import *

# %%
geolocator = Nominatim(user_agent="usrapp")

locDic = {'City': ['Leonessa, PZ', 'Portopalo, SR', 'Messina, ME, IT', 'Barletta, BAT', 'Ischia, NA', 'San Fele, PZ', 'Caltavuturo, PA', 'Siracusa, SR', 'Santeramo in Colle, BA', 'Augusta, SR', 'Sava, TA', 'Torino, TO', 'Avigliano, PZ']}
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
fig,ax = plt.subplots(figsize=(8*1.5,8*1.5))

m = Basemap(resolution='h', projection='merc', 
            llcrnrlat=35, urcrnrlat=47, llcrnrlon=5, urcrnrlon=20)

m.drawcoastlines()
parallels = np.arange(35.,47.,1)
meridians = np.arange(5.,20.01,1)
m.fillcontinents (color='lightgray', lake_color='lightblue')
#parallels = np.arange(35.,45.,1)
m.drawparallels(parallels, labels=[True, True, False, False])
#meridians = np.arange(10.,20.01,1)
m.drawmeridians(meridians, labels=[False, False, True, True])
m.drawmapboundary(fill_color='lightblue')
m.drawcountries()
m.drawstates()

# m.drawcounties()
# x, y = m(*zip(*[hawaii, austin, washington, chicago, losangeles]))

lats = df['Latitude'].to_numpy()
longs = df['Longitude'].to_numpy()
longM, latM = m(longs, lats)

longMinVar, latMinVar = disvarmin(lats, longs)
xx, yy = m(longMinVar, latMinVar)
plt.plot(xx, yy, marker='d', markersize=14, color='r')
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
plt.show()
plt.rcParams.update({'font.size': 16})





