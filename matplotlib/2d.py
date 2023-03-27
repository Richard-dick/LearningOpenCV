import matplotlib.pyplot as plt
import numpy as np

ax = plt.axes(projection='3d')
#从三个维度构建
z = np.linspace(0, 1, 1000)
x = z * np.sin(20 * z)
y = z * np.cos(20 * z)
#调用 ax.plot3D创建三维线图
ax.plot3D(x, y, z, 'red', label='123')
ax.set_title('3D line plot')



plt.legend(loc='best')#图列位置，可选best，center等



plt.show()