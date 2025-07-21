import numpy as np
import csv
import os
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Int16MultiArray, Bool, String

DATA_SAVE = False

class Sensor_Data(Node):
    def __init__(self):
        super().__init__('Sensor_Data')

        # QoS profile for data subscription
        qos_profile = QoSProfile(
            history=HistoryPolicy.KEEP_ALL,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        self.record_state = False
        self.trigger_to_append = False
        self.df = Int16MultiArray()
        self.csv_file_prefix = 'output'
        self.output_dir = '/root/ur5/vibecheck_ws/data/test' # if the saving directory is not defined. This is the default saving directory
        self.message_count = 0
        self.save_status = DATA_SAVE

        # publish data
        self.publisher = self.create_publisher(Int16MultiArray, 'processed_data', 10)
        
        # publish Bool message (control the sweep)        
        self.publisher_s = self.create_publisher(Bool, 'command_topic', 10)

        # subscribe "set_output_dir" topic of type String
        self.dir_sub = self.create_subscription(
            String,
            'set_output_dir',
            self.dir_callback,
            10
        )

        # subscribe to data publisher from teensy (Int16MultiArray messages)
        self.subscription = self.create_subscription(
            Int16MultiArray,
            '/micro_ros_arduino_node_publisher',
            self.listener_callback,
            qos_profile=qos_profile
        )
        
        # subscribe to flag publisher from control.py (it lets us to know when to record data)
        self.subscription_record = self.create_subscription(
            Bool,
            '/record_flag',
            self.flag_callback,
            10
        )

    def dir_callback(self, msg):
        dir_path = msg.data
        self.set_output_dir(dir_path)

    def listener_callback(self, msg):
        if self.trigger_to_append:
            if (not self.record_state):
                processed_msg = Int16MultiArray()
                processed_msg.data = self.df.data
                # print("msg:", processed_msg.data)
                print("msg size:", len(processed_msg.data))
                self.publisher.publish(processed_msg)
                self.get_logger().warn('Recording end. Ignoring message.')
                self.df = Int16MultiArray()
                self.trigger_to_append = False
                return

            self.message_count += 1
            normalized_data = [(x * 1) for x in msg.data]
            if self.save_status:
                #********** Write data into CSV file *************************************
                with open(self.current_csv_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([self.message_count] + normalized_data)
                #*************************************************************************
            self.df.data.extend(normalized_data)
            # print(self.message_count)

    def flag_callback(self, msg):
        self.record_state = msg.data
        print("record_state:", self.record_state)
        if self.record_state:
            self.trigger_to_append = True
            #********** Write data into CSV file *************************************
            if self.save_status:
                self.init_csv_file()
            #*************************************************************************
            msg_s = Bool()
            msg_s.data = True
            self.publisher_s.publish(msg_s)
            self.message_count = 0
            print("trigger_to_append:", self.trigger_to_append)

    def get_unique_csv_file_name(self):
        existing_files = os.listdir(self.output_dir)
        matching_files = [f for f in existing_files if f.startswith(self.csv_file_prefix) and f.endswith('.csv')]

        if not matching_files:
            return f'{self.csv_file_prefix}_1.csv'

        existing_numbers = []
        for file_name in matching_files:
            try:
                number = int(file_name.split('_')[1].split('.')[0])
                existing_numbers.append(number)
            except (ValueError, IndexError):
                continue

        next_number = max(existing_numbers, default=0) + 1
        return f'{self.csv_file_prefix}_{next_number}.csv'

    def init_csv_file(self):
        unique_file_name = self.get_unique_csv_file_name()
        print(self.output_dir)
        csv_file_path = os.path.join(self.output_dir, unique_file_name)
        self.current_csv_file_path = csv_file_path
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['msg'] + [f'data_{i}' for i in range(128)])  # Set data size, the number of columns

    def set_output_dir(self, dir_path: str):
        os.makedirs(dir_path, exist_ok=True)
        self.output_dir = dir_path
        self.get_logger().info(f"Output directory set to: {dir_path}")
    
def main(args=None):
    rclpy.init(args=args)
    node = Sensor_Data()
    rclpy.spin(node)  # Use spin_once to allow shutdown to break the loop

if __name__ == '__main__':
    main()