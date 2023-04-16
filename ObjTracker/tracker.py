import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


def openGen():
    plt.ion()


def closeGen():
    plt.ioff()


class Tracker():
    def __init__(self, path: str = "./params/mtx.npy", upbound: int = 10):
        mtx = np.load(path)
        self.fx = mtx[0][0]
        self.fy = mtx[1][1]
        self.cx = mtx[0][2]
        self.cy = mtx[1][2]
        self.fig = plt.figure(dpi=150)
        self.ax = Axes3D(self.fig, auto_add_to_figure=False)
        self.ax.view_init(elev=18, azim=-85)
        self.fig.add_axes(self.ax)
        self.xs = []
        self.ys = []
        self.zs = []
        self.points = upbound
        self.size = []
        self.color = []
        for i in range(upbound):
            # self.size.append(((i+1)*3.0/float(upbound)) ** 4)
            if i == upbound - 1:
                self.color.append('r')
                self.size.append(25.0)
            else:  # 会反色
                self.color.append('b')
                self.size.append((5 * (i + 1) / float(upbound)) ** 2)

    def get_point3d_from_point2d(self, u: int, v: int, z: np.float32):
        x = float((u - self.cx) * z) / self.fx
        y = float((v - self.cy) * z) / self.fy
        return x, y, z

    def update_points(self, x, y, z):
        if len(self.xs) == 0:
            # 刚开始, 全部设为一个
            self.xs = [x] * self.points
            self.ys = [y] * self.points
            self.zs = [z] * self.points
        else:
            # print(self.xs)
            self.xs = self.xs[1:]
            self.ys = self.ys[1:]
            self.zs = self.zs[1:]
            self.xs.append(x)
            self.ys.append(y)
            self.zs.append(z)
        self.ax.scatter(self.xs, self.zs, self.ys, s=self.size, c=self.color)
        self.ax.plot(self.xs, self.zs, self.ys, 'b-', linewidth=0.5)

    def renew_figure(self):
        # 更新plt
        self.ax.clear()
        # 调整坐标系, 从而更方便观看 xyz --> xz-y
        # X轴正常
        self.ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_xlim(-150, 150)
        # 即正常Y轴变成了Z轴, 作为相机坐标系下的Z轴, 范围0-1500
        self.ax.set_ylabel('Z', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_ylim(0, 1500)
        # 即正常Z轴变成了反向的Y轴, 范围反向150- -150
        self.ax.set_zlabel('Y', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_zlim(150, -150)

    def check(self):
        self.ax.show()

    def get_image(self):
        self.fig.canvas.draw()
        # 转换plt canvas为string，再导入numpy
        vis_img = np.fromstring(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        # 设置numpy数组大小为图像大小
        vis_img.shape = (720, 960, 3)
        # 将RGB格式转换为BGR格式
        vis_img = cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR)
        return vis_img
