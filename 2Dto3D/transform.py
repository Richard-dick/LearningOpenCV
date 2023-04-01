# coding = utf-8

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg
import PIL.Image as Image

# 全局参数
mtx = np.load("params/mtx.npy")
fx = mtx[0][0]
fy = mtx[1][1]
cx = mtx[0][2]
cy = mtx[1][2]

# 创建3D图形
fig = plt.figure(dpi = 150)
ax = Axes3D(fig, auto_add_to_figure=False)
ax.view_init(elev=-74, azim=-90);
fig.add_axes(ax)


# 初始化数据点
xs = []
ys = []
zs = []
upbound = 15

size = []
color = []
for i in range(upbound):
    size.append(((i + 1) * 5.0 / float(upbound)) ** 3)
    if i == upbound - 1:
        color.append('b')
        # self.size.append(25.0)
    else:  # 会反色
        color.append('r')
        # self.size.append((5 * i / float(upbound)) ** 2)


def ShowImage(name, img: np.ndarray ):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


# @param: rgb图像, rgb图像上的uv坐标, 深度图像
def get_point3d_from_point2d(u:int, v:int, z:np.float32):
    global fx, fy, cx, cy
    x = float((u - cx) * z) / fx
    y = float((v - cy) * z) / fy
    return x,y,z


# 创建绘制函数
def update_point(x, y, z):
    global xs, ys, zs, size, color, upbound
    global ax
    ax.clear()
    if len(xs) == 0:
        xs = [x] * upbound
        ys = [y] * upbound
        zs = [z] * upbound
    else:
        xs = xs[1:]
        ys = ys[1:]
        zs = zs[1:]
        xs.append(x)
        ys.append(y)
        zs.append(z)
    ax.scatter(xs, ys, zs, s = size, c = color)
    ax.set_zlabel('Z', fontdict={'size': 10, 'color': 'gray'})
    ax.set_ylabel('Y', fontdict={'size': 10, 'color': 'gray'})
    ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})
    ax.set_zlim(0, 1500)
    ax.set_ylim(-150, 150)
    ax.set_xlim(-150, 150)
    # plt.draw()
    ax.plot(xs, ys, zs, 'r.-', linewidth = 0.5)
    canvas = FigureCanvasAgg(plt.gcf())
    canvas.draw()
    w,h = canvas.get_width_height()
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
