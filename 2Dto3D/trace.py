import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg
import PIL.Image as Image

class Trace():
    def __init__(self, path, upbound = 15):
        mtx = np.load(path)
        self.fx = mtx[0][0]
        self.fy = mtx[1][1]
        self.cx = mtx[0][2]
        self.cy = mtx[1][2]
        self.fig = plt.figure(dpi=150)
        self.ax = Axes3D(self.fig, auto_add_to_figure=False)
        self.ax.view_init(elev=-74, azim=-90);
        self.fig.add_axes(self.ax)
        self.xs = []
        self.ys = []
        self.zs = []
        self.upbound = upbound
        self.size = []
        self.color = []
        for i in range(upbound):
            self.size.append(((i+1)*5.0/float(upbound)) ** 3)
            if i == upbound-1:
                self.color.append('b')
                # self.size.append(25.0)
            else:# 会反色
                self.color.append('r')
                # self.size.append((5 * i / float(upbound)) ** 2)


    def get_point3d_from_point2d(self, u:int, v:int, z:np.float32):
        x = float((u - self.cx) * z) / self.fx
        y = float((v - self.cy) * z) / self.fy
        return x, y, z

    def update_arrs(self, x, y, z):
        if(len(self.xs) == 0):
            # 刚开始, 全部设为一个
            self.xs = [x] * self.upbound
            self.ys = [y] * self.upbound
            self.zs = [z] * self.upbound
        else:
            # print(self.xs)
            self.xs = self.xs[1:]
            self.ys = self.ys[1:]
            self.zs = self.zs[1:]
            self.xs.append(x)
            self.ys.append(y)
            self.zs.append(z)


    def update_point(self, x, y, z):
        # 更新plt
        self.ax.clear()
        # 更新点list
        self.update_arrs(x,y,z)
        # print(len(self.xs))
        # exit(0))
        self.ax.scatter(self.xs, self.ys, self.zs, s = self.size, c = self.color)
        self.ax.set_zlabel('Z', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_ylabel('Y', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})
        self.ax.set_zlim(0, 1500)
        self.ax.set_ylim(-150, 150)
        self.ax.set_xlim(-150, 150)
        # plt.draw()
        self.ax.plot(self.xs, self.ys, self.zs, 'r.-', linewidth=0.5)
        canvas = FigureCanvasAgg(plt.gcf())
        canvas.draw()
        w, h = canvas.get_width_height()
        buf = np.fromstring(canvas.tostring_argb(), dtype=np.uint8)
        buf.shape = (w, h, 4)
        buf = np.roll(buf, 3, axis=2)
        # 得到 Image RGBA图像对象 (需要Image对象的同学到此为止就可以了)
        image = Image.frombytes("RGBA", (w, h), buf.tostring())
        # 转换为numpy array rgba四通道数组
        image = np.asarray(image)
        rgb_image = image[:, :, :3]
        # ShowImage(image,"dd")
        return rgb_image



