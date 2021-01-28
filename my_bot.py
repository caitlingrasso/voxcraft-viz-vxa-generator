import numpy as np
from vxa_generator import vxa_from_array

body = np.zeros((2,2,2)) # body is a 2x2x2 cube
body[:,:,0]=1 # bottom layer is active 
body[:,:,1]=2 # top layer is passive

vxa_from_array(body, save_filename='my_bot.vxa')