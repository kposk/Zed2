import sys
import pyzed.sl as sl
import cv2

measure = sl.Mat()

listpos = [[0, 0]]
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(listpos) > 0:
            listpos.pop(0)
        listpos.append([x, y])
        print(f'[x, y] = {listpos[0]} [PIXEL]\n Distance = {round(measure.get_value(listpos[0][0], listpos[0][1])[1], 4)} [Meter] \n\n')


def main():

    if len(sys.argv) != 2:
        print("Please specify path to .svo file.")
        exit()

    filepath = sys.argv[1]
    print("Reading SVO file: {0}".format(filepath))

    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.coordinate_units = sl.UNIT.METER
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    depth_image = sl.Mat()

    key = ''
    print("  Quit the video reading:     q\n")
    while key != 113:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            cv2.imshow("Left Camera", mat.get_data())
            cam.retrieve_image(depth_image, sl.VIEW.DEPTH)
            cv2.imshow("Depth Image- leftCenter", depth_image.get_data())
            
            cam.retrieve_measure(measure, sl.MEASURE.DEPTH)
            cv2.setMouseCallback('Left Camera', onMouse)

            key = cv2.waitKey(0)
        else:
            key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    print_camera_information(cam)
    cam.close()
    print("\nFINISH")


def print_camera_information(cam):
    while True:
        res = input("Do you want to display camera information? [y/n]: ")
        if res == "y":
            print()
            print("Distorsion factor of the right cam before calibration: {0}.".format(
                cam.get_camera_information().calibration_parameters_raw.right_cam.disto))
            print("Distorsion factor of the right cam after calibration: {0}.\n".format(
                cam.get_camera_information().calibration_parameters.right_cam.disto))

            print("Confidence threshold: {0}".format(cam.get_runtime_parameters().confidence_threshold))
            print("Depth min and max range values: {0}, {1}".format(cam.get_init_parameters().depth_minimum_distance,
                                                                    cam.get_init_parameters().depth_maximum_distance)
)
            print("Resolution: {0}, {1}.".format(round(cam.get_camera_information().camera_resolution.width, 2), cam.get_camera_information().camera_resolution.height))
            print("Camera FPS: {0}".format(cam.get_camera_information().camera_fps))
            print("Frame count: {0}.\n".format(cam.get_svo_number_of_frames()))
            break
        elif res == "n":
            print("Camera information not displayed.\n")
            break
        else:
            print("Error, please enter [y/n].\n")


def saving_image(key, mat):
    if key == 115:
        img = sl.ERROR_CODE.FAILURE
        while img != sl.ERROR_CODE.SUCCESS:
            filepath = input("Enter filepath name: ")
            img = mat.write(filepath)
            print("Saving image : {0}".format(repr(img)))
            if img == sl.ERROR_CODE.SUCCESS:
                break
            else:
                print("Help: you must enter the filepath + filename + PNG extension.")



if __name__ == "__main__":
    main()
