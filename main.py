import sys
import keyboard
import platform_move_functions as pmf
import platform_cinematic as pc

sys.path.append('../')


# Init the printer, gripper and dynamixels
pmf.platform_init()

# Dipping
# chose sheet of data
# start dipping, at the end re ask for a sheet or quit with 'esc'
pc.run_dipping('dipping_parameter.xlsx', 'S2')

# Disconnect all devices
pmf.disconnect_all()
