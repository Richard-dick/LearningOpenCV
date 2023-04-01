import cv2
import numpy as np
import glob

# code from [read://https_blog.csdn.net/?url=https%3A%2F%2Fblog.csdn.net%2Fqq_29931565%2Farticle%2Fdetails%2F119395353]

params_path = "./data/new/"
images_path = "./images/new/"

def calibrate(width:int,height:int, len:np.float32, image_path:str, param_path:str):
    # 预处理
    width = width - 1
    height = height - 1
    images = glob.glob(image_path + "*.jpg")
    # 构建坐标系
    objp = np.zeros((width * height, 3), np.float32)
    objp[:, :2] = np.mgrid[0:height, 0:width].T.reshape(-1, 2)
    objp = len * objp  
    obj_points = []
    img_points = []
    

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (height, width), None)
        if ret:
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
    np.save(param_path + "ret.npy", ret)
    np.save(param_path + "mtx.npy", mtx)
    np.save(param_path + "dist.npy", dist)
    np.save(param_path + "rvecs.npy", rvecs)
    np.save(param_path + "tvecs.npy", tvecs)


    # 内参数矩阵
    return {"ret":ret, "mtx": mtx, "dist": dist,}




if __name__ == '__main__':
    # imagesCap(10, 50)
    # 输入标定的相关参数
    # in_max = calibrate(12, 9, 1.50, images_path, params_path)
    # in_max = calibrate(13, 9, 2.05, images_path, params_path)
    # in_max = calibrate(12, 9, 4.50, images_path, params_path)
    # print(in_max)
    ret = np.load("data/205mm/ret.npy")
    print(ret)
    ret = np.load("data/150mm/ret.npy")
    print(ret)
    ret = np.load("data/new/ret.npy")
    print(ret)
    # ret = np.load("../2Dto3D/params/ret.npy")
    # print(ret)








