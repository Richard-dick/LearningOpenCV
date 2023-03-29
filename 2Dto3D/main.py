import cv2
import numpy as np
import matplotlib.pyplot as plt
from transform import get_point3d_from_point2d, update_point, ShowImage
from trace import Trace

if __name__ == '__main__':
    # image_d = cv2.imread("images/test_d.png")
    # corners = np.load("params/corners.npy")
    # for i in range(corners.shape[0]):
    #     u = corners[i][0]
    #     v = corners[i][1]
    #     x,y,z = get_point3d_from_point2d(u,v,image_d)
    #     update_point(x,y,z)
    # plt.show()
    obj = Trace("params/mtx.npy", 15)
    data = []
    data = np.loadtxt("xyz.txt", dtype=np.float32, delimiter=',')
    for xyz in data:
        x,y,z = obj.get_point3d_from_point2d(xyz[0], xyz[1], xyz[2])
        image = obj.update_point(x,y,z)
        ShowImage(image,'ss')

    # print(data)
