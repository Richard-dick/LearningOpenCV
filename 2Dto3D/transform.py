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
s = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9.6, 10, 11, 12, 13, 14, 15, 16, 17, 18, 25]) * 2
# c = np.array(['b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','r'])
# 会反色
c = np.array(['r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','b'])


def ShowImage(img: np.ndarray, name):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


# @param: rgb图像, rgb图像上的uv坐标, 深度图像
def get_point3d_from_point2d(u:int, v:int, z:np.float32):
    global fx, fy, cx, cy
    # 可能还是三通道, 直接改成单通道并转置
    # if d_image.shape == (720, 1280, 3):
    #     d_image = cv2.cvtColor(d_image, cv2.COLOR_BGR2GRAY)
    #     d_image = d_image.T
    # pixel = d_image[int(u)][int(v)]
    # depth = pixel * 7.8125
    # z = float(depth)
    x = float((u - cx) * z) / fx
    y = float((v - cy) * z) / fy
    return x,y,z

# 创建绘制函数
def update_point(x, y, z):
    global xs, ys, zs, s
    global ax
    ax.clear()
    xs.append(x)
    ys.append(y)
    zs.append(z)
    if len(xs) == 20:
        xs = xs[1:]
        ys = ys[1:]
        zs = zs[1:]
        ax.scatter(xs, ys, zs, s=s, c=c)
    elif len(xs) < 20:
        ax.scatter(xs, ys, zs, c = 'b')
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
