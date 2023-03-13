import cv2
import numpy as np
import math
from vcam import vcam,meshGen

paths = ["./img/fake.png"]

def ShowImage(img : np.ndarray, name):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


for mode in range(1):
    for i, path in enumerate(paths):
        # reading the input image
        img = cv2.imread(path)

        img = cv2.resize(img, (300,300))
        # ShowImage(img, "original")
        H,W = img.shape[:2]
        # print(img.shape)
        # shape give a tuple (high, width, depth)

        c1 = vcam(H=H, W=W)

        plane = meshGen(H,W)
        # print(type(plane))

        if mode == 0:
            plane.Z += 20 * np.exp(-0.5 * ((plane.X * 1.0 / plane.W) / 0.1) ** 2) / (0.1 * np.sqrt(2 * np.pi))
        elif mode == 1:
            plane.Z += 20 * np.exp(-0.5 * ((plane.Y * 1.0 / plane.H) / 0.1) ** 2) / (0.1 * np.sqrt(2 * np.pi))
        elif mode == 2:
            plane.Z -= 10 * np.exp(-0.5 * ((plane.X * 1.0 / plane.W) / 0.1) ** 2) / (0.1 * np.sqrt(2 * np.pi))
        elif mode == 3:
            plane.Z -= 10 * np.exp(-0.5 * ((plane.Y * 1.0 / plane.W) / 0.1) ** 2) / (0.1 * np.sqrt(2 * np.pi))
        elif mode == 4:
            plane.Z += 20 * np.sin(2 * np.pi * ((plane.X - plane.W / 4.0) / plane.W)) + 20 * np.sin(
                2 * np.pi * ((plane.Y - plane.H / 4.0) / plane.H))
        elif mode == 5:
            plane.Z -= 20 * np.sin(2 * np.pi * ((plane.X - plane.W / 4.0) / plane.W)) - 20 * np.sin(
                2 * np.pi * ((plane.Y - plane.H / 4.0) / plane.H))
        elif mode == 6:
            plane.Z += 100 * np.sqrt((plane.X * 1.0 / plane.W) ** 2 + (plane.Y * 1.0 / plane.H) ** 2)
        elif mode == 7:
            plane.Z -= 100 * np.sqrt((plane.X * 1.0 / plane.W) ** 2 + (plane.Y * 1.0 / plane.H) ** 2)
        else:
            print("Wrong mode selected")
            exit(-1)

        pts3d = plane.getPlane()
        # print(type(pts3d)) np.ndarray

        # Projecting (Capturing) the plane in the virtual camera
        pts2d = c1.project(pts3d)
        # print(type(pts2d)) np.ndarray

        # ShowImage(pts3d, "pts3d")
        # ShowImage(pts2d, "pts2d")

        # Deriving mapping functions for mesh based warping.
        map_x, map_y = c1.getMaps(pts2d)
        print(type(map_x))
        # ShowImage(map_y, "map_x")
        print(map_x)

        # Generating the output
        output = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR)
        output = cv2.flip(output, 1)

        cv2.imshow("Funny Mirror", output)
        cv2.imshow("Input and output", np.hstack((img, np.zeros((H, 2, 3), dtype=np.uint8), output)))
        # Uncomment following line to save the outputs
        # cv2.imwrite("Mirror-effect-%d-image-%d.jpg"%(mode+1,i+1),np.hstack((img,np.zeros((H,2,3),dtype=np.uint8),output)))
        cv2.waitKey(0)