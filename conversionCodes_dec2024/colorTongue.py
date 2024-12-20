import numpy as np
import matplotlib.pyplot as plt
import R2cie #### self made library for colorimetry




def gaussian(wavelength, cen, sigmaSq, amp):
    R = amp*np.exp(-((wavelength-cen)**2)/sigmaSq)
    return R

wavelength = np.linspace(350, 800, 1001)

len_sampling = 371*4+1
sampling = np.linspace(380, 750, len_sampling)



fig, (ax1) = plt.subplots(figsize = (4, 4))
fig2, ax2 = plt.subplots(figsize = (4, 4))

ax2.set_xlabel("cie x")
ax2.set_ylabel("cie y")

file = open("color_tongue_boundary.txt", "w")
file.write("#ciex, ciey \n")
file.close()

for i in range(len_sampling):
    R = gaussian(wavelength, cen=sampling[i], sigmaSq=10, amp=1)
    x, y, Y = R2cie.Reflectivity2cie(wavelength, R)
    Y = 0.3
    
    rgb_color = R2cie.xyY_to_rgb(x, y, Y)
    
    ax1.plot(wavelength, R, color = rgb_color, lw = 0.5)
    ax2.plot(x, y,'o', color = rgb_color)
    file = open("color_tongue_boundary.txt", "a")
    file.write(str(x)+"  \t "+ str(y)+"  \n ")
    file.close()



plt.tight_layout()
plt.show()
