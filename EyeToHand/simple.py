import numpy as np
import cv2


def Jet2Gray(false_color_image):
    gray_values = np.arange(256, dtype=np.uint8)
    color_values = map(tuple, cv2.applyColorMap(gray_values, cv2.COLORMAP_JET).reshape(256, 3))
    color_to_gray_map = dict(zip(color_values, gray_values))
    # apply the inverse map to the false color image to reconstruct the grayscale image
    gray_image = np.apply_along_axis(lambda bgr: color_to_gray_map[tuple(bgr)], 2, false_color_image)
    return gray_image


def GetDepth(u, v, in_image):
    image_d = Jet2Gray(in_image)
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
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv.circle(image_rgb, (u, v), 1, (255, 255, 255), -1)
        with open("simple/uv_cam.txt", "a") as f:  # 打开文件
            f.write(str(u)+','+str(v) + '\n')
        cv2.destroyAllWindows()
        # print(u, v)
        # depth = GetDepth(u, v)
        # # print(depth)
        # fx = 896.29746575
        # fy = 896.70309991
        # cx = 649.74499104
        # cy = 373.7277043
        # z = float(depth)
        # x = float((u - cx) * z) / fx
        # y = float((v - cy) * z) / fy
        # print("x:",x,"y:",y,"z:",z)
        # # ShowImage(image_rgb, "image_rgb")

def transformation_matrix(source_points, target_points):
    # 计算源点集和目标点集的质心
    source_centroid = np.mean(source_points, axis=0)
    target_centroid = np.mean(target_points, axis=0)

    # 计算源点集和目标点集的协方差矩阵
    H = np.dot((source_points - source_centroid).T, (target_points - target_centroid))

    # 使用奇异值分解（SVD）计算旋转矩阵R和平移向量t
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)
    t = target_centroid.T - np.dot(R, source_centroid.T)

    # 将旋转矩阵R和平移向量t组合成变换矩阵T
    T = np.identity(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T

def get_point3d_from_point2d(u:int, v:int, z:np.float32):
    fx = 896.29746575
    fy = 896.70309991
    cx = 649.74499104
    cy = 373.7277043
    x = float((u - cx) * z) / fx
    y = float((v - cy) * z) / fy
    with open("simple/xyz_cam.txt", "a") as f:  # 打开文件
        f.write(str(x) + ',' + str(y) + ',' + str(z) + '\n')