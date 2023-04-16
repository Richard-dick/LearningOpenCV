# Obj的tracker

两种方式使用:

## 1 返回图片

见`main.py`中注释掉的代码部分, 

```py
tracker.renew_figure()
img = tracker.update_points(x, y, z)
img = tracker.get_image()
```

第一行更新并重设了坐标轴;
第二行更新点列, 并且执行scatter和plot
第三行画图到canvas上, 并转化成image


## 2 实时显示

见未注释部分, 需要使用openGen(), 也就是打开plt的交互模式, 能够实时出图;

见[iong和ioff](https://blog.csdn.net/weixin_42782150/article/details/107015617)

随后在`update_points`中的每次plot都会更新图片.

pause()防止其过快, 正常使用时不需要


## 3 优化

主要是两个方向

- `ax.clear`的处理, 不知道能不能只清除xs,ys,zs的信息, 保留坐标轴, 这样就很舒服.
- `get_image`的优化, 这里使用的和之前没有太大区别, 还是需要读懂fig中ax的存储格式才行, 但感觉都没有这方面的操作. 兴许这样生成的方法没有实时性的要求, 所以不好优化.






