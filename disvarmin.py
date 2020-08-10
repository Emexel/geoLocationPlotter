import numpy as np

def disvarmin(lats, longs):

    min_lat, max_lat = np.min(lats), np.max(lats)
    parallels = np.arange(35.,42.,0.03)
    meridians = np.arange(10.,20.,0.03)

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

