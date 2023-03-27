from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


# #创建3d绘图区域
# ax = plt.axes(projection='3d')
# #从三个维度构建
# z = np.linspace(0, 10, 10)
# x = z * np.sin(20 * z)
# y = z * np.cos(20 * z)
# #调用 ax.plot3D创建三维线图
# ax.plot3D(x, y, z, 'gray')
# ax.set_title('3D line plot')
# plt.show()

# 限制长度

x = []
y = []
z = []

for i in range(0,15):
    x.append(np.random.uniform(50, 150))
    y.append(np.random.uniform(50, 150))
    z.append(np.random.uniform(50, 150))

fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)
ax.scatter(x,y,z)

# 添加坐标轴
# 添加坐标轴(顺序是Z, Y, X)
ax.set_zlabel('Z', fontdict={'size': 10, 'color': 'gray'})
ax.set_ylabel('Y', fontdict={'size': 10, 'color': 'gray'})
ax.set_xlabel('X', fontdict={'size': 10, 'color': 'gray'})

ax.set_zlim(0,150)
ax.set_ylim(0,150)
ax.set_xlim(0,150)

plt.show()
