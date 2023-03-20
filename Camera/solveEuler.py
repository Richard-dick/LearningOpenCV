import cv2
import numpy as np
import math

def sloveEuler(objp : np.ndarray, Camera_intrinsic: dict):
    obj_points = objp  # 存储3D点
    img_points = []  # 存储2D点

    # 从摄像头获取视频图像
    camera = cv2.VideoCapture(0)

    while True:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        if ret:  # 画面中有棋盘格
            img_points = np.array(corners)
            cv2.drawChessboardCorners(frame, (9, 6), corners, ret)
            # rvec: 旋转向量 tvec: 平移向量
            _, rvec, tvec = cv2.solvePnP(obj_points, img_points, Camera_intrinsic["mtx"],
                                         Camera_intrinsic["dist"])  # 解算位姿
            distance = math.sqrt(tvec[0] ** 2 + tvec[1] ** 2 + tvec[2] ** 2)  # 计算距离
            rvec_matrix = cv2.Rodrigues(rvec)[0]  # 旋转向量->旋转矩阵
            proj_matrix = np.hstack((rvec_matrix, tvec))  # hstack: 水平合并
            eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角
            pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
            cv2.putText(frame, "dist: %.2fcm, yaw: %.2f, pitch: %.2f, roll: %.2f" % (distance, yaw, pitch, roll),
                        (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
                break
        else:  # 画面中没有棋盘格
            cv2.putText(frame, "Unable to Detect Chessboard", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                        (0, 0, 255), 3)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
                break
    cv2.destroyAllWindows()