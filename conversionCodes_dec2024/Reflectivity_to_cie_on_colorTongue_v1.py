import numpy as np
import matplotlib.pyplot as plt
import R2cie #### self made library for colorimetry
from scipy.spatial import ConvexHull

fig, (ax1, ax) = plt.subplots(1, 2, figsize = (8, 4))
wavelength = np.linspace(300, 780, 401)
def gaussian(wavelength, cen, sigma, amp):
    sigmaSq = sigma*sigma
    R = amp*np.exp(-((wavelength-cen)**2)/sigmaSq)
    return R



R = gaussian(wavelength, cen=530, sigma=10, amp=0.99) 
Nx=71 #  THIS CONTROLS THE RESOLUTION OF THE COLOR TONGUE





x, y, Y = R2cie.Reflectivity2cie(wavelength, R)
Y = 0.3
rgb = R2cie.xyY_to_rgb(x, y, Y)

labeltxt = "(%.2f, %.2f)"%(x, y)
ax.plot(x, y, 'o', color = 'black', zorder = 5, label = labeltxt)
ax.legend(frameon = False)
axInset = ax.inset_axes([0.7, 0.65, 0.2, 0.2])
axInset.set_facecolor(rgb)
axInset.set_xticks([])
axInset.set_yticks([])


ax1.plot(wavelength, R, color = 'b', lw = 2)
ax1.set_xlabel("Wavelength (nm)")
ax1.set_ylabel("R ")
ax1.tick_params(axis = 'both', direction = 'in')

##################################################################
################## DO NOT TOUCH HERE #############################
def point_in_hull(point, hull, tolerance=1e-12):
    return all(
        (np.dot(eq[:-1], point) + eq[-1] <= tolerance)
        for eq in hull.equations)

colorTongueBoundary = np.loadtxt("color_tongue_boundary.txt")
x, y = colorTongueBoundary[:, 0], colorTongueBoundary[:, 1]
len_boundary = len(x)
cH = ConvexHull(colorTongueBoundary)

minx = min(x)
maxx = max(x)
miny = min(y)
maxy = max(y)

ux = np.linspace(minx, maxx, Nx)
Ny = int((maxy-miny)*Nx/(maxx-minx))
uy = np.linspace(miny, maxy, Ny)
X, Y = np.meshgrid(ux, uy)



ax.tick_params(axis = 'both', direction = 'in')
ax.set_xlabel("cie x")
ax.set_ylabel("cie y")

for i in range(len_boundary):
    rgb = R2cie.xyY_to_rgb(x[i], y[i], Y=0.3)
    ax.plot(x[i], y[i], '.', color = rgb)
    
    
# point_is_in_hull = point_in_hull(p, hull=cH)
# ax.plot(p[0], p[1], 'o')
# print(point_is_in_hull)
for i in range(Nx):
    for j in range(Ny):
        p = [ux[i], uy[j]]
        point_is_in_hull = point_in_hull(p, hull=cH)
        if(point_is_in_hull):
            rgb = R2cie.xyY_to_rgb(ux[i], uy[j], Y=0.3)
            ax.plot(ux[i], uy[j], '.', color = rgb)
            
##################################################################
###################################################################  





plt.tight_layout()
plt.show()