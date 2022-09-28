import sys
import pyzed.sl as sl
import numpy as np
import cv2


def InitParams():
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Use Ultra depth mode
    init_params.coordinate_units = sl.UNIT.METER
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_minimum_distance = 0.15
    init_params.depth_maximum_distance = 40
    init_params.camera_fps = 60

    return init_params


def RunTimeParams():
    rt_param = sl.RuntimeParameters()
    rt_param.sensing_mode = sl.SENSING_MODE.STANDARD
    rt_param.confidence_threshold = 100
    rt_param.textureness_confidence_threshold = 100

    return rt_param

listpos = [[0, 0]]
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(listpos) > 0:
            listpos.pop(0)
        listpos.append([x, y])

def main():
    init_params = InitParams()
    rt_param = RunTimeParams()

    zed = sl.Camera()
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        sys.stdout.write(repr(err))
        zed.close()
        exit()

    Depth_image = sl.Mat()
    Left_image = sl.Mat()
    measure = sl.Mat()

    while 1:

        if zed.grab(rt_param) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(Depth_image, sl.VIEW.DEPTH)
            depth_image_rgba = Depth_image.get_data()
            depth_image = cv2.cvtColor(depth_image_rgba, cv2.COLOR_RGBA2RGB)
            cv2.imshow('depth', depth_image)

            zed.retrieve_measure(measure, sl.MEASURE.DEPTH)
            cv2.setMouseCallback('depth', onMouse)

            print(f'[x, y] = {listpos[0]} [PIXEL]||| Distance = {round(measure.get_value(listpos[0][0], listpos[0][1])[1], 4)} [METER]')
            #print(f'distance = {measure.get_value(xg, yg)}, x = {xg}, y = {yg}')

            #zed.retrieve_image(Left_image, sl.VIEW.LEFT)
            #image_left = Left_image.get_data()
            #image_left = cv2.cvtColor(image_left, cv2.COLOR_RGBA2RGB)
            #cv2.imshow('image', image_left)

            cv2.waitKey(5)

    zed.close()


if __name__ == "__main__":
    main()
