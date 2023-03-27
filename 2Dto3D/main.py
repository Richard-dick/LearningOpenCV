# coding = utf-8

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 全局参数
mtx = np.load("params/mtx.npy")
fx = mtx[0][0]
fy = mtx[1][1]
cx = mtx[0][2]
cy = mtx[1][2]

# 创建3D图形
fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

# 初始化数据点
xs = []
ys = []
zs = []

def ShowImage(img: np.ndarray, name):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


# @param: rgb图像, rgb图像上的uv坐标, 深度图像
def get_point3d_from_point2d(u:int, v:int, d_image:np.ndarray):
    global fx, fy, cx, cy
    # 可能还是三通道, 直接改成单通道并转置
    if d_image.shape == (720, 1280, 3):
        d_image = cv2.cvtColor(d_image, cv2.COLOR_BGR2GRAY)
        d_image = d_image.T
    pixel = d_image[int(u)][int(v)]
    depth = pixel * 7.8125
    z = float(depth)
    x = float((u - cx) * z) / fx
    y = float((v - cy) * z) / fy
    return x,y,z

# 创建绘制函数
def update_point(x, y, z):
    global xs, ys, zs
    global ax
    if len(xs) == 10:
        xs = xs[1:]
        ys = ys[1:]
        zs = zs[1:]
    xs.append(x)
    ys.append(y)
    zs.append(z)
    ax.clear()
    ax.scatter(xs, ys, zs)
    ax.set_zlabel('Z', fontdict={'size': 10, 'color': 'gray'})
    ax.set_ylabel('Y', fontdict={'size': 10, 'color': 'gray'})
    ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})
    ax.set_zlim(0, 1500)
    ax.set_ylim(-150, 150)
    ax.set_xlim(-150, 150)
    plt.draw()
    plt.pause(0.01)


if __name__ == '__main__':
    image_d = cv2.imread("images/test_d.png")
    corners = np.load("params/corners.npy")
    for i in range(corners.shape[0]):
        u = corners[i][0]
        v = corners[i][1]
        x,y,z = get_point3d_from_point2d(u,v,image_d)
        update_point(x,y,z)
    plt.show()

    # ShowImage(image_rgb, "image_rgb")
    # plt.show()
