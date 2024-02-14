import cv2
from djitellopy import tello
from time import sleep
from threading import Thread, Event
from random import randint
from sdf import face_match

# Create the drove object.
my_drone = tello.Tello()

# Connect to the drone.
my_drone.connect()
turn_the_drone_flag = True


def turn_around(turn_around_cm_amount: int):
    """ The function Gets a number of degrees to turn around the drone. """
    while turn_the_drone_flag:
        my_drone.rotate_clockwise(turn_around_cm_amount)


def capture_image():
    """ Start to streaming and sending each frame to the enemy_recognition() func to check if an enemy is in the img,
        if yes, then it will stop the drone from turning around and call the function to kill the enemy. """
    global turn_the_drone_flag
    # Start streaming.
    my_drone.streamon()

    # This loop send every frame to the "" function.
    while True:
        img = my_drone.get_frame_read().frame

        # with open("new_image.jpg", "w") as file:
        #     file.write(img)

        cv2.imshow("Image", img)

        if face_match(img, "elya.jpg"):
            turn_the_drone_glag = False  # It terminates the Turning of the drone.
            print("Mached!")

        if randint(0, 9000) == 25:
            turn_the_drone_flag = False  # It terminates the Turning of the drone.
            print("randd...")
        cv2.waitKey(1)


def kill_the_enemy():
    # Moving forward until the collision.
    my_drone.move_forward(500)


def main():
    print(my_drone.get_battery())

    # Taking the drone up.
    my_drone.takeoff()
    my_drone.move_up(90)
    # set the speed of the drone
    my_drone.set_speed(50)

    # Thread initialize for turning the drone.
    turning_drone_thread = Thread(target=turn_around, args=(20,))
    turning_drone_thread.start()

    # Start recording from the drone.
    capture_image()

    turning_drone_thread.join()

    # land the drone
    my_drone.send_rc_control(0, 0, 0, 0)
    my_drone.land()
    my_drone.streamoff()


if __name__ == "__main__":
    main()
