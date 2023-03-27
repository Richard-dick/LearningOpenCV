import cv2
import numpy as np
import math

def solveEuler(width:int,height:int, len:np.float32):
    # 预处理
    width = width - 1
    height = height - 1
    mtx = np.load("params/mtx.npy")
    dist = np.load("params/dist.npy")
    # 构建坐标系
    objp = np.zeros((height * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)
    objp = len * objp
    obj_points = objp  # 存储3D点

    frame = cv2.imread("images/test/test_rgb.jpg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (width, height), None)
    if ret:  # 画面中有棋盘格
        img_points = np.array(corners)
        cv2.drawChessboardCorners(frame, (width, height), corners, ret)
        # rvec: 旋转向量 tvec: 平移向量
        _, rvec, tvec = cv2.solvePnP(obj_points, img_points, mtx, dist)  # 解算位姿
        distance = math.sqrt(tvec[0] ** 2 + tvec[1] ** 2 + tvec[2] ** 2)  # 计算距离
        rvec_matrix = cv2.Rodrigues(rvec)[0]  # 旋转向量->旋转矩阵
        proj_matrix = np.hstack((rvec_matrix, tvec))  # hstack: 水平合并
        eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角
        pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
        cv2.putText(frame, "dist: %.2fcm, yaw: %.2f, pitch: %.2f, roll: %.2f" % (distance, yaw, pitch, roll),
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('frame', frame)
    else:  # 画面中没有棋盘格
        cv2.putText(frame, "Unable to Detect Chessboard", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                    (0, 0, 255), 3)
        cv2.imshow('frame', frame)
    # print(corners.reshape(-1,2))
    np.save('corners.npy',corners.reshape(-1,2))
    cv2.waitKey()
    cv2.destroyAllWindows()