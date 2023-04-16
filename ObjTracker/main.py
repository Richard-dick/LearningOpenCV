import cv2
import numpy as np
import matplotlib.pyplot as plt
from tracker import Tracker, openGen, closeGen
import time


if __name__ == '__main__':
    tracker = Tracker()
    data = []
    data = np.loadtxt("xyz.txt", dtype=np.float32, delimiter=',')
    openGen()

    for xyz in data:
        x, y, z = tracker.get_point3d_from_point2d(xyz[0], xyz[1], xyz[2])
        t1 = time.time()

        tracker.renew_figure()
        img = tracker.update_points(x, y, z)
        plt.pause(0.001)

        print(time.time() - t1)

    closeGen()
    plt.show()


# if __name__ == '__main__':
#     tracker = Tracker()
#     data = []
#     data = np.loadtxt("xyz.txt", dtype=np.float32, delimiter=',')
#     for xyz in data:
#         x, y, z = tracker.get_point3d_from_point2d(xyz[0], xyz[1], xyz[2])
#
#         t1 = time.time()
#         tracker.renew_figure()
#         img = tracker.update_points(x, y, z)
#         img = tracker.get_image()
#
#         print(time.time() - t1)
#         cv2.imshow("ss", img)
#         cv2.waitKey()
#
#     exit(0)