import sys
import pyzed.sl as sl
import numpy as np
import cv2
import keyboard


def InitParams():
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.camera_fps = 60

    return init_params


def RunTimeParams():
    rt_param = sl.RuntimeParameters()
    rt_param.sensing_mode = sl.SENSING_MODE.STANDARD
    rt_param.confidence_threshold = 100
    rt_param.textureness_confidence_threshold = 100

    return rt_param


i, j = 1, 1
def onMouse(event, x, y, flags, param,):
    if event == cv2.EVENT_LBUTTONDOWN:
        global i, j

        Right_image = sl.Mat()
        zed.retrieve_image(Right_image, sl.VIEW.RIGHT)
        right_image_CV = Right_image.get_data()

        Left_image = sl.Mat()
        zed.retrieve_image(Left_image, sl.VIEW.LEFT)
        left_image_CV = Left_image.get_data()

        nameright = "/home/vant3d/Pictures/" + "ImageRIGHT" + str(i) + ".jpg"
        nameleft = "/home/vant3d/Pictures/" + "ImageLEFT" + str(j) + ".jpg"

        i = i + 1
        j = j + 1

        cv2.imwrite(nameright, right_image_CV)
        cv2.imwrite(nameleft, left_image_CV)


zed = sl.Camera()


def main():
    init_params = InitParams()
    rt_param = RunTimeParams()

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        sys.stdout.write(repr(err))
        zed.close()
        exit()

    image = sl.Mat()

    while 1:

        if zed.grab(rt_param) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.SIDE_BY_SIDE)
            image_rgba = image.get_data()
            imagergb = cv2.cvtColor(image_rgba, cv2.COLOR_RGBA2RGB)
            cv2.imshow('Both Images', imagergb)

            cv2.setMouseCallback('Both Images', onMouse)

            cv2.waitKey(5)

    zed.close()


if __name__ == "__main__":
    main()
