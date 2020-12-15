import scipy.optimize
import numpy as np


px = [24.42, 24.33, 515.95, 515.95]
py = [299.53, -41.64, -41.63, 301.53]
pn = len(px)

def circle_fit(input):
    xm = input[0]
    ym = input[1]
    r = input[2]

    err = 0
    for i in range(pn):
        err += (np.sqrt((px[i]-xm)**2+(py[i]-ym)**2)-r)**2

    return err


sol = scipy.optimize.minimize(circle_fit, [1,1,1])
xm = round(sol.x[0],6)
ym = round(sol.x[1],6)
r = round(sol.x[2],6)
print("xm = {}, ym = {}, r = {}".format(xm, ym, r))