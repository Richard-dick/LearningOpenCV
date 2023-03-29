import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制3D图像

x = np.random.standard_normal(100)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)

trace = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5))
ax.plot(x, y, z, c='r')
data = [trace]
layout = go.Layout(scene=dict(xaxis=dict(title='X'), yaxis=dict(title='Y'), zaxis=dict(title='Z')), width=700, height=700)

fig = go.Figure(data=data, layout=layout)
fig.write_html('test.html')