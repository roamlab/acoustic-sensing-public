import os
import time
from dynamixel_sdk import *  # Uses Dynamixel SDK library

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Fin_control():
    def __init__(self):
        # Control table address
        self.ADDR_PRO_TORQUE_ENABLE      = 64
        self.ADDR_PRO_GOAL_POSITION      = 116
        self.ADDR_PRO_PRESENT_POSITION   = 132
        self.ADDR_PRO_PRESENT_CURRENT    = 126
        self.ADDR_OPERATING_MODE         = 11
        self.ADDR_HARDWARE_ERROR_STATUS  = 70  # Hardware error status
        self.ADDR_PRO_GOAL_CURRENT       = 102
        self.ADDR_PRO_CURRENT_LIMIT      = 38

        # Protocol version
        self.PROTOCOL_VERSION            = 2.0

        # Default setting
        self.DXL_ID                      = 1
        self.BAUDRATE                    = 57600
        self.DEVICENAME                  = '/dev/ttyUSB0'

        self.TORQUE_ENABLE               = 1
        self.TORQUE_DISABLE              = 0
        self.DXL_MINIMUM_POSITION_VALUE  = 1125 # when gripper is opened 1660
        self.DXL_MAXIMUM_POSITION_VALUE  = 1800 # when gripper is closed 2570 1790
        self.DXL_MOVING_STATUS_THRESHOLD = 20

        self.OPERATING_MODE_CURRENT_BASED_POSITION = 5
        self.GOAL_CURRENT_VALUE = 200 # about 2.69[mA]
        self.CURRENT_LIMIT_VALUE = 1000  # about 2.69[mA]

        self.index = 0
        self.dxl_goal_position = [self.DXL_MAXIMUM_POSITION_VALUE, self.DXL_MINIMUM_POSITION_VALUE]

        # Initialize PortHandler instance
        self.portHandler = PortHandler(self.DEVICENAME)

        # Initialize PacketHandler instance
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            # getch()
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            # getch()
            quit()

        # Set control mode for Dynamixel
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_OPERATING_MODE, self.OPERATING_MODE_CURRENT_BASED_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel is now in current-based position control mode")

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRO_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")

        # Set goal current
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRO_GOAL_CURRENT, self.GOAL_CURRENT_VALUE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Goal current has been successfully set to %d" % self.GOAL_CURRENT_VALUE)

    def check_hardware_error(self):
        # Read Hardware Error Status
        dxl_hardware_error, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_HARDWARE_ERROR_STATUS)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        # Check for specific hardware errors
        if dxl_hardware_error != 0:
            print("Hardware Error Detected: 0x%02X" % dxl_hardware_error)
            if dxl_hardware_error & 0x01:
                print("Input Voltage Error")
            if dxl_hardware_error & 0x02:
                print("Overheating Error")
            if dxl_hardware_error & 0x04:
                print("Motor Encoder Error")
            if dxl_hardware_error & 0x08:
                print("Electrical Shock Error")
            if dxl_hardware_error & 0x10:
                print("Overload Error")
        else:
            print("No Hardware Error")
            
    def close_gripper(self):
        print("Press any key to continue! (or press ESC to quit!)")
        index=0
        # Write goal position
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRO_GOAL_POSITION, self.dxl_goal_position[index])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def open_gripper(self):
        index=1
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRO_GOAL_POSITION, self.dxl_goal_position[index])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        time.sleep(1)
        # dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRO_TORQUE_ENABLE, self.TORQUE_DISABLE)
        # if dxl_comm_result != COMM_SUCCESS:
        #     print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        # elif dxl_error != 0:
        #     print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        
            
def main():

        
    temp=Fin_control()

    temp.close_gripper()

    time.sleep(2)

    temp.open_gripper()
if __name__ == "__main__":
    main()
