from skimage import data, color, io, img_as_float, feature
import numpy as np
import matplotlib.pyplot as plt

def img_with_bw_boundaries(img, BW, alpha=1):

    edge = feature.canny(BW)    
    img_rgb = color.grey2rgb(img)
    img_R = img_rgb[:,:,0]
    img_R[edge] = 255
    img_rgb[:,:,0] = img_R
    img_masked = img_rgb
    
    return img_masked
