import numpy as np
import cv2 as cv
from evaluate import solveEuler


def ShowImage(img: np.ndarray, name):
    cv.imshow(name, img)
    cv.waitKey()
    cv.destroyAllWindows()


def LoadParam():
    mtx = np.load("params/mtx.npy")
    # print(type(mtx))
    # print(mtx)
    fx = mtx[0][0]
    fy = mtx[1][1]
    cx = mtx[0][2]
    cy = mtx[1][2]
    # print(fx, fy, cx, cy)
    return fx,fy,cx,cy

def Gen3DCor():
    pass


def GetDepth(u, v):
    image_d = cv.imread("images/test/test_d.png")
    image_d = cv.cvtColor(image_d, cv.COLOR_RGB2GRAY)
    # 记得转置, 不然行列对不上
    image_d = image_d.T
    # print(image_d.shape[-1])
    # exit(0)
    pixel = image_d[u][v]
    depth = pixel * 7.8125
    return depth
    # ShowImage(image_d, "image_d")


def GetCoordinate(event, u, v, flags, param):
    # 单击选取像素点
    if event == cv.EVENT_LBUTTONDOWN:
        # cv.circle(image_rgb, (u, v), 1, (255, 255, 255), -1)
        print("u,v:",u, v)
        depth = GetDepth(u, v)
        # print(depth)
        fx,fy,cx,cy = LoadParam()
        z = float(depth)
        x = float((u - cx) * z) / fx
        y = float((v - cy) * z) / fy
        print("x:",x,"y:",y,"z:",z)
        # ShowImage(image_rgb, "image_rgb")



if __name__ == '__main__':
    solveEuler(13, 9, 2.05)
    image_rgb = cv.imread("images/test/test_rgb.jpg")

    # 绑定窗口和回调函数
    cv.namedWindow("image_rgb")
    cv.setMouseCallback('image_rgb', GetCoordinate)
    ShowImage(image_rgb, "image_rgb")

