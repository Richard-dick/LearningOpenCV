import cv2
import numpy as np
import matplotlib.pyplot as plt
from transform import get_point3d_from_point2d, update_point

if __name__ == '__main__':
    # image_d = cv2.imread("images/test_d.png")
    # corners = np.load("params/corners.npy")
    # for i in range(corners.shape[0]):
    #     u = corners[i][0]
    #     v = corners[i][1]
    #     x,y,z = get_point3d_from_point2d(u,v,image_d)
    #     update_point(x,y,z)
    # plt.show()
    data = []
    data = np.loadtxt("xyz.txt", dtype=np.float32, delimiter=',')
    for xyz in data:
        x,y,z = get_point3d_from_point2d(xyz[0], xyz[1], xyz[2])
        update_point(x,y,z)
    plt.show()

    # print(data)
