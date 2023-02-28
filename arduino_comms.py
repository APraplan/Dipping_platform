import serial.tools.list_ports

class arduino:
    def _init_(self, descriptiveDeviceName, portName, baudrate):
        self.descriptiveDeviceName = descriptiveDeviceName
        self.serialInst = serial.Serial()
        self.serialInst.baudrate = baudrate
        self.serialInst.port = portName
        self.serialInst.open()
    
    def command(self, com):
        self.serialInst.write(com.encode('utf-8'))