from dynamixel_sdk import *

class XL430:
    def __init__(self, id, servo_port = "/dev/ttyUSB1", buad_rate = 1000000, mode = 'v') -> None:
        self._servo_port = servo_port
        self._baud_rate = buad_rate
        self._id = id
        
        self._portHandler = PortHandler(self._servo_port)
        self._portHandler.openPort()
        self._portHandler.setBaudRate(self._baud_rate)
        
        self._handler = Protocol2PacketHandler()
        
        self._handler.write1ByteTxRx(self._portHandler, self._id, 64, 0)
        
        if mode == 'v':
            self._handler.write1ByteTxRx(self._portHandler, self._id, 11, 1)
        elif mode == 'p':
            self._handler.write1ByteTxRx(self._portHandler, self._id, 11, 3)
            
    def set_rpm(self, rpm):
        if rpm == 0:
            self.set_torque_enable(False)
            self._handler.write4ByteTxRx(self._portHandler, self._id, 104, 0)
        elif abs(rpm) <= 60.69:
            self.set_torque_enable(True)
            self._handler.write4ByteTxRx(self._portHandler, self._id, 104, int(rpm*265/60.69))
            return True
        return False
        
    def set_torque_enable(self, torque):
        if torque == True:
            self._handler.write1ByteTxRx(self._portHandler, self._id, 64, 1)
            return True
        elif torque == False:
            self._handler.write1ByteTxRx(self._portHandler, self._id, 64, 0)
            return True
        return False
        
        
    def get_rpm(self):
        current_rpm, _, _ = self._handler.read4ByteTxRx(self._portHandler, self._id, 128)
        return current_rpm*0.229
    
    def get_position(self):
        current_position, _, _ = self._handler.read4ByteTxRx(self._portHandler, self._id, 132)
        return current_position*0.087891
    
    def get_pwm(self):
        current_pwm, _, _ = self._handler.read2ByteTxRx(self._portHandler, self._id, 124)
        return current_pwm*0.11299
    
    def get_load(self):
        current_load, _, _ = self._handler.read2ByteTxRx(self._portHandler, self._id, 126)
        return current_load*0.1
    
    def get_voltage(self):
        current_voltage, _, _ = self._handler.read1ByteTxRx(self._portHandler, self._id, 144)
        return current_voltage*0.1
    
    def get_temperature(self):
        current_temperature, _, _ = self._handler.read1ByteTxRx(self._portHandler, self._id, 146)
        return current_temperature

xl = XL430(1)
xl.set_rpm(0)