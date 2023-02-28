import keyboard
from time import sleep

while True:

    if keyboard.is_pressed('enter'):
        print('enter')
    if keyboard.is_pressed('a'):
        print('a')

    sleep(0.02)