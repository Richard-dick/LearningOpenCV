import cv2
import numpy as np


def Jet2Gray(false_color_image):
    gray_values = np.arange(256, dtype=np.uint8)
    color_values = map(tuple, cv2.applyColorMap(gray_values, cv2.COLORMAP_JET).reshape(256, 3))
    color_to_gray_map = dict(zip(color_values, gray_values))
    # apply the inverse map to the false color image to reconstruct the grayscale image
    gray_image = np.apply_along_axis(lambda bgr: color_to_gray_map[tuple(bgr)], 2, false_color_image)
    return gray_image



# depth_p_name = './XXX.jpg'
# im_depth = cv2.imread(depth_p_name)
# gray_img = Jet2Gray(im_depth)
# gray = gray_img/255
# gray = gray*2000