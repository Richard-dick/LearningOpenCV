# Calibrate

这是一个简单的标定程序

## interface

```py
def calibrate(
    width:int,      # 宽有多少个方块
    height:int,     # 高有多少方块
    len:np.float32, # 格子尺寸
    image_path:str, # 图像位置
    param_path:str  # 参数保存位置
    isDraw:bool     # 是否画出图像
    )
```

## realization

### preprocessing
```py
# 按规范-1
width = width - 1
height = height - 1
# 读入image, 创建一个list
images = glob.glob(image_path + "*.jpg")
```

### build a ??
```py
# 构建一个width * height行的 3列的 float32型矩阵
objp = np.zeros((width * height, 3), np.float32)
# 首先构建第一个height行 width列 二维数组:
    # 为行序+1, 如[0,0][1,1][2,2]
    # 构造第二个, 列序, 如[0,1][0,1][0,1]
    # 拼装到一起 构成一个3维矩阵, 索引顺序为x(0);y(height);z(width)
    # 3维转置后是z->y->x 详见参考网站
    # reshape(-1,2)是指不管行有多少, 列为2, 按索引排序
# 随后赋给objp的前两位, 也就是xy序列
# 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
objp[:, :2] = np.mgrid[0:height, 0:width].T.reshape(-1, 2)  
# 打印棋盘格一格的边长(厘米单位)
objp = len * objp  
obj_points = []  # 存储3D点
img_points = []  # 存储2D点
```

### process

```py
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = gray.shape[::-1] # 起到一个转置的作用, 因为calibrateCamera需要
    ret, corners = cv2.findChessboardCorners(gray, (height, width), None)
    if ret: # 如果找到了, 进一步亚像素角点检测
        obj_points.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1),
                                    (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001))
        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)
        cv2.drawChessboardCorners(img, (9, width), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
        cv2.waitKey(1)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
```

### save

```py
np.save(param_path + "ret.npy", ret)
np.save(param_path + "mtx.npy", mtx)
np.save(param_path + "dist.npy", dist)
np.save(param_path + "rvecs.npy", rvecs)
np.save(param_path + "tvecs.npy", tvecs)
```











## reference

[np中三维数组转置](https://blog.csdn.net/u014041590/article/details/89159638)