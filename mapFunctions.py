import numpy as np
from mpl_toolkits.basemap import Basemap

def disvarmin(lats, longs):

    min_lat, max_lat = np.min(lats), np.max(lats)
    min_long, max_long = np.min(longs), np.max(longs)
    num_steps = 250

    parallels = np.arange(min_lat ,max_lat, abs(min_lat - max_lat)/num_steps)
    meridians = np.arange(min_long ,max_long, abs(min_long - max_long)/num_steps)

    # disvar = 1e15
    latMin = np.array([])
    longMin = np.array([])
    var = np.array([])

    for pars in parallels:
        for mers in meridians:
            sd = (np.max(np.sqrt((lats - pars)**2 + (longs - mers)**2)) - np.min(np.sqrt((lats - pars)**2 + (longs - mers)**2)))**2
            #if sd<disvar:
            var = np.append(var, sd)
            latMin = np.append(latMin, pars)
            longMin = np.append(longMin, mers)

    idm = np.argmin(var)
    longMin = longMin[np.argmin(var)]
    latMin = latMin[np.argmin(var)]

    return(longMin, latMin)


def drawMap(lats, longs, quality='c'):

    min_lat, max_lat = np.min(lats), np.max(lats)
    min_long, max_long = np.min(longs), np.max(longs)

    subdivisions = 10
    lat_scale, long_scale = 0.1, 0.2 

    # plot limits: 1 - lower left lat ; 2 - upper right lat ; 3 - lower left lon ; 4 - upper right lon
    plot_limits = np.zeros(4)

    if min_lat < 0:
        plot_limits[0] = min_lat * (1 + lat_scale)
    else:
        plot_limits[0] = min_lat * (1 - lat_scale)
    
    if min_long < 0:
        plot_limits[2] = min_long * (1 + long_scale)
    else:
        plot_limits[2] = min_long * (1 - long_scale)
#  ---------
    if max_lat < 0:
        plot_limits[1] = max_lat * (1 - lat_scale)
    else:
        plot_limits[1] = max_lat * (1 + lat_scale)
    
    if max_long < 0:
        plot_limits[3] = max_long * (1 - long_scale)
    else:
        plot_limits[3] = max_long * (1 + long_scale)


    if plot_limits[2] < -180:
        plot_limits[2] = -180
    if plot_limits[3] > 180:
        plot_limits[3] = 180
    
    print(plot_limits)

    # print('Latitude extremes:', min_lat, max_lat)
    # print('Long extremes:', min_long, max_long)

    m = Basemap(resolution=quality, projection='merc', 
            llcrnrlat=plot_limits[0], urcrnrlat=plot_limits[1],
            llcrnrlon=plot_limits[2], urcrnrlon=plot_limits[3])

    m.drawcoastlines()
    m.fillcontinents (color='lightgray', lake_color='lightblue')
    m.drawmapboundary(fill_color='lightblue')
    m.drawcountries()
    # m.drawstates()

    parallels = np.round(np.linspace(np.round(plot_limits[0]), np.round(plot_limits[1]), subdivisions))
    meridians = np.round(np.linspace(np.round(plot_limits[2]), np.round(plot_limits[3]), subdivisions))
    # parallels = np.arange(np.round(plot_limits[0]), np.round(plot_limits[1]), subdivisions)
    # meridians = np.arange(np.round(plot_limits[2]), np.round(plot_limits[3]), subdivisions)
    # np.linspace(min_lat, max_lat, subdivisions)
    # np.linspace(min_long, max_long, subdivisions)
    
    m.drawparallels(parallels, labels=[True, True, False, False])
    m.drawmeridians(meridians, labels=[False, False, True, True])

    return m