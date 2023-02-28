from time import sleep, time
from printer_comms import printer
from comms_wrapper_grip import *
from dynamixel_controller import Dynamixel
import sys
import keyboard
import platform_coordinates as pc

sys.path.append('../')

# Used variables
# Ports need to be changed to match the ports used on the computer
gripper = Arduino(descriptiveDeviceName="ARD1", portName="COM11", baudrate=9600)
anycubic = printer(descriptive_device_name="printer", port_name="COM13", baudrate=115200)
dyna = Dynamixel(ID=[1, 2], descriptive_device_name="XL430 test motor", series_name=["xl", "xl"], baudrate=57600,
                 port_name="COM12")


def platform_init():
    # Ask the user to remove all glasses and vials before initializing
    print("Please remove all glasses and vials from the printer before initializing")
    print('Press "Enter" to start zeroing')
    print("")
    keyboard.wait("enter")
    print("Zeroing")
    print("")

    # Home position for the dynamixels
    dyna.begin_communication()
    dyna.set_operating_mode("position", ID="all")
    dyna.write_profile_acceleration(5, ID="all")
    dyna.write_profile_velocity(150, ID="all")
    # 0 corresponds to "gripper up" position
    dyna.write_position(0, ID=1)
    sleep(0.2)

    # Home position for the printer
    anycubic.connect()
    # Set the speed of the printer to maximum (100mm/s)
    anycubic.move_speed(speed=100)
    anycubic.move_datum()
    print('Press "Enter" when printer is at origin')
    keyboard.wait("enter")

    anycubic.set_home_pos(0, 104, 140)
    anycubic.move_home()
    print('Press "Enter" when printer is at home point and the glass and vials are placed')
    keyboard.wait("enter")

    # Home position for the dynamixels
    # 2051 corresponds to "gipper upside down" position
    dyna.write_position(2051, ID=1)
    sleep(3)
    # 2051 corresponds to "gipper fingers aligned with glass" position
    dyna.write_position(54, ID=2)
    sleep(3)

    # Home position for the gripper
    gripper.connect_and_handshake()
    sleep(0.5)
    gripper.send_message("open")
    sleep(2)
    # disconnect from the gripper
    gripper.disconnect_arduino()


def disconnect_all():
    anycubic.disconnect()
    gripper.disconnect_arduino()
    dyna.end_communication()
    print('Goodbye ;)')


# Lib
# anycubic.move_axis_absolute(x=None, y=None, z=none, f=None, printMsg=False)
# dyna.write_position(2051, ID=1) max 4096 ?
# gripper.send_message("close")


def dip_once(glass_plate, solution):

    # Wait until the gripper is at a safe height
    anycubic.move_axis_absolute(x=None, y=None, z=pc.SAFE_MOVE_HEIGHT, f=None, printMsg=False)
    while anycubic.read_position()[2] != pc.SAFE_MOVE_HEIGHT:
        pass

    # Rotate the gripper down
    dyna.write_position(pc.DOWN, ID=1)

    # Move on the solution
    anycubic.move_axis_absolute(x=solution.x, y=solution.y, z=None, f=None, printMsg=False)
    while not (anycubic.read_position()[0] == solution.x and anycubic.read_position()[1] == solution.y):
        pass

    # Dip
    anycubic.move_axis_absolute(x=None, y=None, z=solution.z, f=None, printMsg=False)
    while anycubic.read_position()[2] != solution.z:
        pass

    sleep(glass_plate.dipping_time)

    anycubic.move_axis_absolute(x=None, y=None, z=pc.SAFE_MOVE_HEIGHT, f=None, printMsg=False)
    while anycubic.read_position()[2] != pc.SAFE_MOVE_HEIGHT:
        pass

    glass_plate.number_of_dip += 1


def dip_cycle(glass_plate, solution1, solution2, clean_solution):
    while not glass_plate.expected_dip == glass_plate.number_of_dip:

        dip_once(glass_plate, solution1)

        if glass_plate.clean == 'y':
            dip_once(glass_plate, clean_solution)

        dip_once(glass_plate, solution2)


def store(glass_plate):

    # Wait until the gripper is at a safe height
    anycubic.move_axis_absolute(x=None, y=None, z=pc.SAFE_MOVE_HEIGHT, f=None, printMsg=False)
    while anycubic.read_position()[2] != pc.SAFE_MOVE_HEIGHT:
        pass

    # Left side
    if glass_plate.num <= 5:

        # Move at a safe rotation position
        if anycubic.read_position()[0] < pc.MIN_X_FOR_ROTATION:
            anycubic.move_axis_absolute(x=pc.MIN_X_FOR_ROTATION, y=None, z=None, f=None, printMsg=False)
            while not (anycubic.read_position()[0] == pc.MIN_X_FOR_ROTATION):
                pass

        # Rotate the gripper left flat
        dyna.write_position(pc.LEFT, ID=1)
        dyna.write_position(pc.ANGLE_MINUS_90, ID=2)

    # Right side
    else:

        # Move at a safe rotation position
        if anycubic.read_position()[0] > pc.MAX_X_FOR_ROTATION:
            anycubic.move_axis_absolute(x=pc.MAX_X_FOR_ROTATION, y=None, z=None, f=None, printMsg=False)
            while not (anycubic.read_position()[0] == pc.MAX_X_FOR_ROTATION):
                pass

        # Rotate the gripper right flat
        dyna.write_position(pc.RIGHT, ID=1)
        dyna.write_position(pc.ANGLE_90, ID=2)

    # Go to right height
    if glass_plate.num == 1 or 6:
        height = pc.HEIGHT_STORE_1
    elif glass_plate.num == 2 or 7:
        height = pc.HEIGHT_STORE_2
    elif glass_plate.num == 3 or 8:
        height = pc.HEIGHT_STORE_3
    elif glass_plate.num == 4 or 9:
        height = pc.HEIGHT_STORE_4
    elif glass_plate.num == 5 or 10:
        height = pc.HEIGHT_STORE_5

    anycubic.move_axis_absolute(x=None, y=None, z=height, f=None, printMsg=False)
    while anycubic.read_position()[2] != height:
        pass


def take(glass_plate):
    pass


def manual_control():
    
    print('Press Q to quit')
    
    speed = 10
    
    Dynamixel.set_operating_mode("velocity", ID = 'all')

    while True:
        
        # Quit
        if keyboard.is_pressed("q"):
            break
        
        # Speed
        if keyboard.is_pressed("1"):
            speed = 10
        
        if keyboard.is_pressed("2"):
            speed = 100
        
        # Anycubic
        if keyboard.is_pressed('r'):
            anycubic.read_position()
            print('Dynamixel 1: ', Dynamixel.read_position(ID = 1))
            print('Dynamixel 2: ', Dynamixel.read_position(ID = 2))
            while keyboard.is_pressed('r'):
                pass
              
        if keyboard.is_pressed('a'):
            anycubic.move_x_speed(-speed)
            while keyboard.is_pressed('a'):
                pass
            anycubic.abort_motion()
            
        if keyboard.is_pressed('d'):
            anycubic.move_x_speed(speed)
            while keyboard.is_pressed('d'):
                pass
            anycubic.abort_motion()
            
        if keyboard.is_pressed('w'):
            anycubic.move_y_speed(speed)
            while keyboard.is_pressed('w'):
                pass
            anycubic.abort_motion()
            
        if keyboard.is_pressed('s'):
            anycubic.move_y_speed(-speed)
            while keyboard.is_pressed('s'):
                pass
            anycubic.abort_motion()
            
        if keyboard.is_pressed('e'):
            anycubic.move_z_speed(speed)
            while keyboard.is_pressed('e'):
                pass
            anycubic.abort_motion()
    
        if keyboard.is_pressed('c'):
            anycubic.move_z_speed(-speed)
            while keyboard.is_pressed('c'):
                pass
            anycubic.abort_motion()
            
        # Dynamixel
        if keyboard.is_pressed('j'):
            Dynamixel.write_velocity(speed, ID = 1)
            while keyboard.is_pressed('j'):
                pass
            Dynamixel.write_velocity(0, ID = 1)
            
        if keyboard.is_pressed('l'):
            Dynamixel.write_velocity(-speed, ID = 1)
            while keyboard.is_pressed('l'):
                pass
            Dynamixel.write_velocity(0, ID = 1)
              
        if keyboard.is_pressed('i'):
            Dynamixel.write_velocity(speed, ID = 2)
            while keyboard.is_pressed('i'):
                pass
            Dynamixel.write_velocity(0, ID = 2)
            
        if keyboard.is_pressed('k'):
            Dynamixel.write_velocity(-speed, ID = 2)
            while keyboard.is_pressed('k'):
                pass
            Dynamixel.write_velocity(0, ID = 2)
        
        sleep(0.02)
        
    Dynamixel.set_operating_mode("position", ID = 'all')
