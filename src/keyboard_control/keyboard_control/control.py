import csv
import os
import time
from classifior import Classifior
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from example_interfaces.srv import AddTwoInts, Trigger
from std_msgs.msg import Int16MultiArray, Bool

class Sensor_Data_Trigger(Node):
    def __init__(self):
        super().__init__('Sensor_Data_Trigger')

        # QoS profile for data subscription
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )
        
        self.df=[]
        self.callback_group = MutuallyExclusiveCallbackGroup()

        # publish bool to let data_collector.py know when to start collecting data
        self.publisher = self.create_publisher(Bool, 'record_flag', 10)

        # subscribe data from data_collector.py
        self.subscription = self.create_subscription(
            Int16MultiArray,
            '/processed_data',
            self.listener_callback,
            qos_profile=qos_profile,
            callback_group=self.callback_group
        )
        
    def start_record(self):
        msg = Bool()
        msg.data = True
        self.publisher.publish(msg)

    def stop_record(self):
        msg = Bool()
        msg.data = False
        self.publisher.publish(msg)

    def listener_callback(self, msg):
        # send data as long vector (combine all msgs with one long vector)
        if self.df is None:
            return
        normalized_data = [(x * 1) for x in msg.data]
        self.df = normalized_data

    def get_data(self):
        return self.df

class CommandAndDataCollector(Node):
    def __init__(self,data_collector,classifier):
        super().__init__('command_and_data_collector1')

        self.classifier=classifier
        self.data_collector=data_collector

        self.results = self.create_service(Trigger, 'results', self.service_reuturn_state) 
        
    def publish_command(self):
        self.data_collector.start_record()
        time.sleep(1)
        self.data_collector.stop_record()
 
    def get_df(self):
        return self.data_collector.get_data()
    
    def get_state_from_data(self):
        self.publish_command()
        time.sleep(0.5)
        data=self.get_df()
        print(data,len(data))
        self.classifier.set_data(data)
        self.classifier.processData()
        label=self.classifier.predict_label()
        
        return label    
    
    def service_reuturn_state(self, request, response):
        label=self.get_state_from_data()
        response.success=True
        response.message=label
        return response

def main(args=None):
    rclpy.init(args=args)
    sensor=Sensor_Data_Trigger()
    model_folder = "/root/ur5/vibecheck_ws/model/"
    classifier = Classifior(model_path=model_folder)
    classifier.load_model("MLP_train_demo_process_fixed_pca_parm_below_21000_02_28", "KPCA_train_demo_process_fixed_pca_parm_below_21000_02_28")
    node = CommandAndDataCollector(sensor,classifier)
    executor = MultiThreadedExecutor(num_threads=3)
    
    executor.add_node(sensor)
    executor.add_node(node)
    executor.spin()        

if __name__ == '__main__':
    main()