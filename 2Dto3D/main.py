import cv2
import numpy as np
import matplotlib.pyplot as plt
from transform import get_point3d_from_point2d, update_point, ShowImage
from trace import Trace
from evaluate import evaluate
from jet2gray import Jet2Gray

# if __name__ == '__main__':
#     # image_d = cv2.imread("images/test_d.png")
#     # corners = np.load("params/corners.npy")
#     # for i in range(corners.shape[0]):
#     #     u = corners[i][0]
#     #     v = corners[i][1]
#     #     x,y,z = get_point3d_from_point2d(u,v,image_d)
#     #     update_point(x,y,z)
#     # plt.show()
#     data = []
#     data = np.loadtxt("xyz.txt", dtype=np.float32, delimiter=',')
#     for xyz in data:
#         x,y,z = get_point3d_from_point2d(xyz[0], xyz[1], xyz[2])
#         image = update_point(x,y,z)
#         ShowImage(image,'ss')


rgb_list = ["rgb_2023_03_27_15_36_38_671.jpg",
"rgb_2023_03_27_15_36_39_471.jpg",
"rgb_2023_03_27_15_36_40_271.jpg",
"rgb_2023_03_27_15_36_41_072.jpg",
"rgb_2023_03_27_15_36_41_871.jpg",
"rgb_2023_03_27_15_36_42_671.jpg",
"rgb_2023_03_27_15_36_43_472.jpg",
"rgb_2023_03_27_15_36_44_272.jpg",
"rgb_2023_03_27_15_36_45_071.jpg",
"rgb_2023_03_27_15_36_45_872.jpg",
"rgb_2023_03_27_15_36_46_671.jpg",
"rgb_2023_03_27_15_36_47_472.jpg",
"rgb_2023_03_27_15_36_48_271.jpg",
"rgb_2023_03_27_15_36_49_072.jpg",
"rgb_2023_03_27_15_36_49_871.jpg",
"rgb_2023_03_27_15_36_50_672.jpg",
"rgb_2023_03_27_15_36_51_472.jpg",
"rgb_2023_03_27_15_36_52_271.jpg",
"rgb_2023_03_27_15_36_53_072.jpg",
"rgb_2023_03_27_15_36_53_871.jpg",
"rgb_2023_03_27_15_36_54_671.jpg",
"rgb_2023_03_27_15_36_55_472.jpg",
"rgb_2023_03_27_15_36_57_072.jpg",
"rgb_2023_03_27_15_36_57_872.jpg",
"rgb_2023_03_27_15_36_58_671.jpg",
"rgb_2023_03_27_15_36_59_471.jpg",
"rgb_2023_03_27_15_37_00_271.jpg",
"rgb_2023_03_27_15_37_01_071.jpg",
"rgb_2023_03_27_15_37_01_872.jpg"]
jet_list = ["d_2023_03_27_15_36_38_671.png",
"d_2023_03_27_15_36_39_471.png",
"d_2023_03_27_15_36_40_271.png",
"d_2023_03_27_15_36_41_072.png",
"d_2023_03_27_15_36_41_871.png",
"d_2023_03_27_15_36_42_671.png",
"d_2023_03_27_15_36_43_472.png",
"d_2023_03_27_15_36_44_272.png",
"d_2023_03_27_15_36_45_071.png",
"d_2023_03_27_15_36_45_872.png",
"d_2023_03_27_15_36_46_671.png",
"d_2023_03_27_15_36_47_472.png",
"d_2023_03_27_15_36_48_271.png",
"d_2023_03_27_15_36_49_072.png",
"d_2023_03_27_15_36_49_871.png",
"d_2023_03_27_15_36_50_672.png",
"d_2023_03_27_15_36_51_472.png",
"d_2023_03_27_15_36_52_271.png",
"d_2023_03_27_15_36_53_072.png",
"d_2023_03_27_15_36_53_871.png",
"d_2023_03_27_15_36_54_671.png",
"d_2023_03_27_15_36_55_472.png",
"d_2023_03_27_15_36_57_072.png",
"d_2023_03_27_15_36_57_872.png",
"d_2023_03_27_15_36_58_671.png",
"d_2023_03_27_15_36_59_471.png",
"d_2023_03_27_15_37_00_271.png",
"d_2023_03_27_15_37_01_071.png",
"d_2023_03_27_15_37_01_872.png"]

if __name__ == '__main__':
    all_e = 0.0
    for i in range(29):
        print("round", i, ":")
        rgb_name = rgb_list[i]
        jet_name = jet_list[i]
        rgb_image = cv2.imread("images/rgb/" + rgb_name)
        # ShowImage("rgb", rgb_image)

        jet_image = cv2.imread("images/jet/" + jet_name)
        depth_image = Jet2Gray(jet_image).T
        # ShowImage("depth", depth_image)
        # # ShowImage("depth", depth_image)
        tvec = evaluate(12, 9, 35.0, rgb_image)
        ref_x = tvec[0][0]
        ref_y = tvec[1][0]
        ref_z = tvec[2][0]
        corners = np.load("params/corners.npy")
        u = int(corners[0][0])
        v = int(corners[0][1])

        depth = depth_image[u][v] * 7.8125
        x,y,z = get_point3d_from_point2d(u,v,depth)
        e_x = abs((ref_x - x) / ref_x)
        e_y = abs((ref_y - y) / ref_y)
        e_z = abs((ref_z - z) / ref_z)
        print("ref_x:", ref_x, "|| x", x, "|| error_x:", e_x)
        print("ref_y:", ref_y, "|| y", y, "|| error_y:", e_y)
        print("ref_z:", ref_z, "|| z", z, "|| error_z:", e_z)
        e = (e_x+e_y+e_z)/3
        print("avg_error:", e)
        all_e = all_e + e

    all_e = all_e / 29
    print("all_error:", all_e)



