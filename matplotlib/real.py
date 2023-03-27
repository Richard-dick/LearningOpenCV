import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# 初始化数据点
xs = []
ys = []
zs = []

# 创建绘制函数
def update_point(x, y, z):
    global xs, ys, zs
    global ax
    if len(xs) == 10:
        xs = xs[1:]
        ys = ys[1:]
        zs = zs[1:]
    xs.append(np.random.uniform(50, 150))
    ys.append(np.random.uniform(50, 150))
    zs.append(np.random.uniform(50, 150))
    ax.clear()
    ax.scatter(xs, ys, zs)
    ax.set_zlabel('Z', fontdict={'size': 10, 'color': 'gray'})
    ax.set_ylabel('Y', fontdict={'size': 10, 'color': 'gray'})
    ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})
    ax.set_zlim(0, 150)
    ax.set_ylim(0, 150)
    ax.set_xlim(0, 150)
    plt.draw()
    plt.pause(0.01)

# 测试绘制函数
for i in range(1000):
    update_point(i/100, i/100, i/100)

plt.show()
