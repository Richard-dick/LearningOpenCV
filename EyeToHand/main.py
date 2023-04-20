import numpy as np
import cv2
from simple import *
import glob

# mtx = [[896.29746575,   0.,         649.74499104]
#  [  0.,         896.70309991, 373.7277043 ]
#  [  0.,           0.,           1.,        ]]








if __name__ == '__main__':

    # images = glob.glob("simple/camera/rgb/*.jpg")
    # for fname in images:
    #     # 绑定窗口和回调函数
    #     image = cv2.imread(fname)
    #     cv2.namedWindow("image_rgb")
    #     cv2.setMouseCallback('image_rgb', GetCoordinate)
    #     cv2.imshow("image_rgb", image)
    #     cv2.waitKey()

    # d_images = glob.glob("simple/camera/depth/*.png")
    # data = np.loadtxt("simple/uv_cam.txt", dtype=np.int32, delimiter=',')
    # for fname, uv in zip(d_images, data):
    #     print(fname, uv)
    #     image = cv2.imread(fname)
    #     depth = GetDepth(uv[0], uv[1], image)
    #     get_point3d_from_point2d(uv[0], uv[1], depth)

    ros_points = np.loadtxt("simple/xyz_ros.txt", dtype=np.float32, delimiter=',')
    cam_points = np.loadtxt("simple/xyz_cam.txt", dtype=np.float32, delimiter=',')
    T1 = transformation_matrix(ros_points, cam_points)
    print(T1)
    # T2 = transformation_matrix(cam_points, ros_points)
    # print(T2)
    # print(r1)
    for i in range(10):
        print("round", i)
        print("ros_p:", ros_points[i])
        test = np.append(ros_points[i], np.array([1]))
        res = np.matmul(T1, test)
        print("trans:", res[:3])
        print("target:", cam_points[i])

    # test = cam_points[0]
    # print("cam_p:", test)
    # res = np.matmul(test, T1) + r1
    # print("after trans:", res)
    # print("target:", ros_points[0])
    # for i in range(10):
    #     print("round", i)
    #     test = cam_points[i]
    #     test = np.append(test, np.array([1]))
    #     print("cam_p:",test)
    #     res = np.matmul(T1, test)
    #     print("trans:", res)
    #     print("target:", ros_points[i])



