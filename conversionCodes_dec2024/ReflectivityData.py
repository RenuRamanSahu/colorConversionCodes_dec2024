import numpy as np
import matplotlib.pyplot as plt
import R2cie #### self made library for colorimetry
from  mpl_toolkits.axes_grid1.inset_locator  import (inset_axes, InsetPosition, mark_inset)
from matplotlib.patches import Rectangle

data = np.genfromtxt('R_data_900_25nm_Ga_spheres_strainPercent00_xpsan2um_yspan1p2um.txt', delimiter = ',')
wavelength =  data[:, 0]
R = data[:, 1]


def gaussian(wavelength, cen, sigmaSq, amp):
    R = amp*np.exp(-((wavelength-cen)**2)/sigmaSq)
    return R

R = gaussian(wavelength, cen=380, sigmaSq=9, amp=1)

#Smoothing Data
N = 1
wavelength = np.convolve(wavelength, np.ones(N)/N, 'valid')
R = np.convolve(R, np.ones(N)/N, 'valid')


fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 5))
ax1.plot(wavelength, R)
ax1.set_xlabel(r'$\lambda$ (nm)')
ax1.set_ylabel('R')



I = plt.imread("CIE_xyY40percent.tiff")
I = I[100:1000, 0:800 ]
ax2.imshow(I, extent = [0.1, 0.8, 0, 0.9])
ax2.set_xlabel('CIE x')
ax2.set_ylabel('CIE y')
x, y, Y = R2cie.Reflectivity2cie(wavelength, R)
ax2.plot(x, y, '.', color = 'black', alpha = 1)
ax2.text(0.55, 0.78, "("+str("{:.2f}".format(x))+", "+str("{:.2f}".format(y))+")")
Y = 0.3

rgb = R2cie.xyY_to_rgb(x, y, Y)
HSV = R2cie.RGB_to_HSV(rgb[0],rgb[1], rgb[2])
ax3 = plt.axes([0, 0, 1, 1])
ip = InsetPosition(ax2, [0.65,0.700,0.16,0.12])
ax3.set_axes_locator(ip)
ax3.set_xticks([])
ax3.set_yticks([])
ax3.set_frame_on(False)
rect = Rectangle((0, 0), 1, 1, facecolor = rgb, edgecolor = rgb)
ax3.add_patch(rect)


plt.tight_layout()
plt.show()
