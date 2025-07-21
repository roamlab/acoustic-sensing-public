import numpy as np
import time
from pynput import keyboard
from MLP_policy import *
from classifior import Classifior
from collections import Counter
from fin_control import Fin_control
from control import CommandAndDataCollector, Sensor_Data_Trigger
from threading import Thread, Event
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from example_interfaces.srv import AddTwoInts, Trigger

class ActionPublisher(Node):
    def __init__(self, keyboard_input):
        super().__init__('robot_command_publisher')
        self.get_logger().info('robot interface')
        self.keyboard_input = keyboard_input
        
        self.cli = self.create_client(AddTwoInts, 'ur5_control')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()
        self.req.b = 0
        
        self.results = self.create_client(Trigger, 'results')
        while not self.results.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')       
        self.trigger = Trigger.Request()
        self.Fin_control = Fin_control()
        
    def get_keyboard(self, key, extra=None):
        """Update the current pose and publish it."""
        if(key=='d'):                         # Go Down with contact detection
            temp = self.send_request(1)
            print('Move down')
            # print(temp.sum)
        elif(key=='u'):                       # Go UP
            temp = self.send_request(2)
            print('Lift up')
        elif(key=='z'):                       # Rotate on z-axis (positive angle)
            temp = self.send_request(3)
            print('rotate along z axis in forward direction')
        elif(key=='x'):                       # Rotate on x-axis (negative angle)
            temp = self.send_request(4)
            print('rotate along x axis in forward direction')
        elif(key=='n'):                       # Rotate on z-axis (negative angle)
            temp = self.send_request(5)
            print('rotate along z axis in backward direction')
        elif(key=='m'):                       # Rotate on x-axis (positive angle)
            temp = self.send_request(6)
            print('rotate along x axis in backward direction')
        elif(key=='i'):                       # Go to initial pose
            temp = self.send_request(7)
            print('move to initial pose')
        elif(key=='a'):                       # Compute z pose in mm                            
            temp = self.send_request(8)
        elif(key=='t'):                       # Compute euler pose [x,y,z]
            temp = self.send_request(9)
        elif(key=='r'):                       # Go to random initial pose
            temp = self.send_request(10)
        elif(key=="e"):                       # Go to initial pose (to prepare the experiments)
            temp = self.send_request(11)
        elif(key=="j"):                       # Go to inital pose (for different tasks)
            temp = self.send_request(12)
        elif(key==","):                       # Rotate on y-axis (positive angle)
            temp = self.send_request(13)
        elif(key=="."):                       # Rotate on y-axis (negative angle)
            temp = self.send_request(14)
        elif(key=='l'):                       # Assign random angle on z-axis
            temp = self.send_request(15)
        elif(key=='c'):                       # Collect data & predict label
            print(self.get_results())
        elif(key=='g'):                       # Close gripper
            print(self.Fin_control.close_gripper())
        elif(key=='o'):                       # Open gripper
            print(self.Fin_control.open_gripper()) 
        elif(key=='s'):                       # Run hard coded demo
            # self.keyboard_input.start_process()
            # self.keyboard_input.start_process_five_sweeps()
            self.keyboard_input.start_process_history_all_case()
        elif(key=='p'):                       # Auto data collection process for peg-in-hole insertion task
            self.keyboard_input.demo_data_collect()    
        elif(key=='b'):                       # Deploy trained policy
            self.keyboard_input.deploy_policy() 
        elif(key=='h'):                       # Test trained model
            self.keyboard_input.test_model()
        elif(key=='/'):                       # Auto data collection process for material property, grasping point, and internal structure
            self.keyboard_input.material_grasppoing_internalstructure_estimation_task_data_collection()
        else:    
            print("no define "+key)
    
    def send_request(self, a):
        self.req.a = a
        return self.cli.call(self.req)
    
    def get_results(self):
        return self.results.call(self.trigger)

class KeyboardInput(Thread):
    def __init__(self, action_publisher):
        super().__init__()
        self.stop_event = Event()
        self.active_keys = set()
        self.action_publisher=action_publisher
        
        self.dir_pub = self.action_publisher.create_publisher(String, 'set_output_dir', 10)
        
        ## For data_collecting proecess
        model_folder = "/root/ur5/vibecheck_ws/model/"
        result_path="/root/ur5/vibecheck_ws/policy/"
        self.output_dir = '/root/ur5/vibecheck_ws/src/Vibecheck_Control/data'
        sensor = Sensor_Data_Trigger()
        classifier = Classifior(model_path=model_folder)
        self.Control = CommandAndDataCollector(sensor,classifier)
        self.Fin_control = Fin_control()
        self.obs = Observation() 
        self.mlp_agant = MLP_Agent(input_size=self.obs.observation_size, output_size=5, hidden_size=128,result_path=result_path)
        self.mlp_agant.load_model()

################################## Given #######################################       
    def stop(self):
        """Stop the thread."""
        self.stop_event.set().message  
        self.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def on_press(self, key):
        """Handle key press events."""
        try:
            pass
        except AttributeError:
            pass

    def on_release(self, key):
        """Handle key release events."""
        try:
            key_name = key.char if hasattr(key, 'char') else key.name
            # self.active_keys.discard(key_name)
            self.action_publisher.get_keyboard(key_name)
        except AttributeError:
            pass

    def run(self):
        
        """Run the thread."""
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()   # Polling frequency
        
#################################################################################        

############################# heuristic-based exploration policy #############################
    def start_process(self):
        # true_label=['diagonal_2points', 'diagonal_2points', 'diagonal_2points', 'one_line', 'one_line', 'one_line', 'one_surface']

        while True:
            self.action_publisher.get_keyboard('d') # go down and detect contact
            time.sleep(1)
            label = self.action_publisher.get_results().message # collect data and classify label
            # time.sleep(1.1)
            # label=true_label[index] # assign label
            print(label)
            
            if label == 'diagonal_2points':
                self.action_publisher.get_keyboard('u') # go up
                time.sleep(1)
                self.action_publisher.get_keyboard('z') # rotate along z axis
                time.sleep(1)
                

            elif label == 'one_line':
                self.action_publisher.get_keyboard('u') # go up
                time.sleep(1)
                self.action_publisher.get_keyboard('x') # ritate akibg x axis
                time.sleep(1)

            elif label == 'one_surface':
                # time.sleep(0.5)
                print('Task completed')
                self.Fin_control.open_gripper()
                time.sleep(1)
                # print('Task completed')
                return
            
    def start_process_five_sweeps(self):
        
        while True:
            labels = []
            for i in range(5):
                self.action_publisher.get_keyboard('d') # go down and detect contact
                time.sleep(1)
                label = self.action_publisher.get_results().message # collect data and classify label
                labels.append(label)
                print(label)
                self.action_publisher.get_keyboard('u') # go up
                time.sleep(1)
                
            print(labels)
            # Count the occurrences of each label
            label_counts = Counter(labels)

            # Find the most common label
            most_common_label, count = label_counts.most_common(1)[0]
            print(most_common_label)
            
            if most_common_label == 'diagonal_2points':
                self.action_publisher.get_keyboard('u') # go up
                time.sleep(1)
                self.action_publisher.get_keyboard('z') # rotate along z axis
                time.sleep(1)
                

            elif most_common_label == 'one_line':
                self.action_publisher.get_keyboard('u') # go up
                time.sleep(1)
                self.action_publisher.get_keyboard('x') # ritate akibg x axis
                time.sleep(1)

            elif most_common_label == 'one_surface':
                # time.sleep(0.5)
                print('Task completed')
                self.Fin_control.open_gripper()
                time.sleep(1)
                # print('Task completed')
                return
    
    def collect_data(self):
        self.action_publisher.get_keyboard('d') 
        label = self.action_publisher.get_results().message  
        self.action_publisher.get_keyboard('u')
        time.sleep(1)  

        return label
    
    def collect_data_for_in_hole(self):
        self.action_publisher.get_keyboard('d') 
        time.sleep(1)
        label = self.action_publisher.get_results().message  
        self.action_publisher.get_keyboard('u')
        time.sleep(1)  

        return label  
    
    def move_forward(self, label):
        if label == 'diagonal_2points':
            self.action_publisher.get_keyboard('z')

        elif label == 'one_line':
            self.action_publisher.get_keyboard('x')
        else:
            time.sleep(1)
        # return exp
            
    def move_backward(self, label):
        if label == 'diagonal_2points':
            self.action_publisher.get_keyboard('n')  # Rotate a.message  long z-axis backward

        elif label == 'one_line':
            self.action_publisher.get_keyboard('m')  # Rotate along x-axis backward
        else:
            time.sleep(1)
        # return exp

    def start_process_history(self):
        previous_labels = []
        
        while True:
            current_label = self.collect_data()
            print(f"Current label: {current_label}")
            previous_labels.append(current_label)
            
            self.move_forward(current_label)
            
            next_label = self.collect_data()
            print(f"Next label: {next_label}")
            previous_labels.append(next_label)

            print(f"Combined labels: {previous_labels}")

            label_counts = Counter(previous_labels)
            most_common_label, _ = label_counts.most_common(1)[0]
            print(f"Most common label: {most_common_label}")

            if most_common_label == 'diagonal_2points':
                if current_label == 'diagonal_2points':
                    print('correct z action')
                else:
                    self.move_backward(current_label)

            elif most_common_label == 'one_line':
                if current_label == 'one_line':
                    print('correct x action')
                else:
                    self.move_backward(current_label)

            elif current_label == 'one_surface':
                print("Task completed: Reached one_surface state.")
                self.action_publisher.get_keyboard('d') 
                time.sleep(2)
                self.Fin_control.open_gripper()
                return
            
            previous_labels = [current_label]  # Keep only the label from current pose for the next iteration
            print(f"Updated previous labels: {previous_labels}")
            
    def start_process_history_all_case(self):
        history = {}
        full_history = []
        # full_poses = []
        history['previous'], history['current'], history['next'] = None, None, None
        actions_taken = []  # list of actions ('diagonal' (z action) or 'one_line' (x action)) taken and not redone (i.e. we did not move backwards)
        x_phase = False  # becomes True once we think we're in the x rotation phase
        x_actions_to_x_phase = 2
        correction_labels = []
        
        while True:
            count_diagonal_2points = full_history.count('diagonal_2points')
            count_one_line = full_history.count('one_line')
            time.sleep(0.1)
            if count_diagonal_2points == 10 and count_one_line == 10:
                current_label = self.collect_data_for_in_hole()
                # print(f"CURRENT LABEL: {current_label}")
                history['current'] = current_label
                current_action = current_label         
            else:
                current_label = self.collect_data()
                # print(f"CURRENT LABEL: {current_label}")
                history['current'] = current_label
                current_action = current_label
            
            
            # if full_history.count('diagonal_2points') == 10 and current_label == 'diagonal_2points':
            #     print('resetting...')
            #     index = 0
            #     for i, label in enumerate(reversed(full_history)):
            #         if label == 'one_line':
            #             index = i
            #             break
            #         self.move_backward(label)
            #     # pose = full_poses[-index]
            #     # self.action_publisher.get_keyboard('p')
            #     full_history = full_history[:-index+1]
            #     # full_poses = full_poses[:-index+1]
            #     if index + 1 < len(full_history): 
            #         history['previous'] = full_history[-index - 1]
            #     continue
            
            if full_history.count('diagonal_2points') == 10 and current_label == 'diagonal_2points':
                print('possibly current label. analyzing current label...')
                self.action_publisher.get_keyboard('n')
                for i in reversed(range(len(full_history))):
                    if full_history[i] == 'diagonal_2points':
                        full_history.pop(i)
                        break
                    
                for i in range(5):
                    time.sleep(0.1)
                    correction_label = self.collect_data()
                    correction_labels.append(correction_label)
                label_counts = Counter(correction_labels)
                most_common_label, _ = label_counts.most_common(1)[0]
                print(f"Most common label: {most_common_label}")
                
                history['current'] = most_common_label
                current_action = most_common_label
                current_label = most_common_label
                correction_labels = []
                continue
                
            # if full_history.count('diagonal_2points') == 10 and current_label == 'diagonal_2points':
            #     print("Resetting... moving back to the state right BEFORE the first 'one_line'")

            #     one_line_index = None
            #     for i, label in enumerate(full_history):
            #         if label == 'one_line':
            #             one_line_index = i
            #             break
                
            #     if one_line_index is not None:
            #         if one_line_index == 0:
            #             print("Earliest label is already 'one_line'; there's no prior state to go back to.")
            #             self.action_publisher.get_keyboard('i')
            #         else:
            #             self.action_publisher.get_keyboard('i')

            #             actions_to_replay = full_history[:one_line_index]
            #             for lbl in actions_to_replay:
            #                 self.move_forward(lbl)
            #             full_history = actions_to_replay

            #             if full_history:
            #                 history['previous'] = full_history[-1]
            #             else:
            #                 history['previous'] = None
            #     else:
            #         print("No 'one_line' found in history, cannot reset to it.")

            #     continue
            
            action_correct = True
            
            if x_phase:
                current_action = 'one_line'
                
            current_pose = self.move_forward(current_action)
            
            time.sleep(0.1)
            if count_diagonal_2points == 10 and count_one_line == 10:
                next_label = self.collect_data_for_in_hole()
            else:
                next_label = self.collect_data()
                
            # print(f"NEXT LABEL: {next_label}")
            history['next'] = next_label

            print('x_phase: ', x_phase)
            # print('actions_taken: ', actions_taken)
            
            print("history: ", history)
            # print(f"Combined labels: {history}")
            print('full history:', full_history)
                    
            if ('diagonal' in history['next']) and not x_phase:
                if 'diagonal' in history['current']:
                    print('correct z action')
                elif 'one_line' in history['current']:
                    action_correct = False
                elif 'one_surface' in history['current']:
                    action_correct = False
                    
            elif ('diagonal' in history['next']) and x_phase:
                action_correct = False

            if 'one_line' in history['next']:
                if ('diagonal' in history['current']) and not x_phase:
                    print('correct z action')
                elif ('diagonal' in history['current']) and x_phase:
                    action_correct = False
                        
                elif 'one_line' in history['current']:
                    print('correct x action')
                elif 'one_surface' in history['current']:
                    action_correct = False

            if 'one_surface' in history['next']:
                if 'diagonal' in history['current']:  
                    action_correct = False
                elif 'one_line' in history['current']:
                    ('correct x action')
                elif 'one_surface' in history['current']:
                    print('found hole!')
                    
            if 'one_surface' in history['current']:
                if 'one_surface' in history['previous']:
                    print("Task completed: Reached one_surface state.")
                    time.sleep(2)
                    self.action_publisher.get_keyboard('d') 
                    time.sleep(1)
                    self.Fin_control.open_gripper()
                    return
                    
            previous_labels = [current_label]  # Keep only the label from current pose for the next iteration
            # print(f"Updated previous labels: {previous_labels}")
        
            if action_correct:
                history['previous'] = history['current']
                actions_taken.append(current_label)
                # full_poses.append(current_pose)
                full_history.append(current_label)
                print('action was correct')
            else:
                print('action was incorrect')
                self.move_backward(current_action)
                
                for i in range(5):
                    time.sleep(0.1)
                    correction_label = self.collect_data()
                    correction_labels.append(correction_label)
                label_counts = Counter(correction_labels)
                most_common_label, _ = label_counts.most_common(1)[0]
                print(f"Most common label: {most_common_label}")
                
                self.move_forward(most_common_label)
                history['previous'] = history['current']
                actions_taken.append(most_common_label)
                full_history.append(most_common_label)
                correction_labels = []
                
            history['current'] = None
            history['next'] = None
            
            # if actions_taken.count('one_line') == x_actions_to_x_phase:
                # x_phase = True
                # print('setting x_phase to True')
                
            print('-----') 
        
    def get_pose(self):
        pose = self.ee.tcp_pose()
        return pose 

    def data_collection_csv(self):
        
        for i in range(10):

            self.action_publisher.get_keyboard('g')
            time.sleep(3)
            self.action_publisher.get_keyboard('d') # go down and detect contact
            # for i in range(5):
            # self.action_publisher.get_results()
            self.action_publisher.get_keyboard('u') # go up
            time.sleep(2)
            self.action_publisher.get_keyboard('o')
            time.sleep(1)

        print("100 Collection Done")

#################################################################################################

############################# imitation learning policy #############################       
    def get_current_z_coordinate(self):
        response = self.action_publisher.send_request(8)

        z_in_meters = response.sum
        # print(z_in_meters)
        return z_in_meters
    
    def move_to_in_hole_pose(self):
        self.action_publisher.get_keyboard('i')
        for i in range(10):
            self.action_publisher.get_keyboard('z')
        for i in range(10):
            self.action_publisher.get_keyboard('x')

    def robot_move(self, next_action):
        text = ''
        if next_action == 0:
            self.action_publisher.get_keyboard('z')
            text = 'z'
            return text
        elif next_action == 1:
            self.action_publisher.get_keyboard('x')
            text = 'x'
            return text

    def deploy_policy(self):
        inserted = False
        labels = []
        actions = []
        process = "in_progress"
        phase = 'general'
        label = None
        
        self.action_publisher.get_keyboard("i")
        self.action_publisher.get_keyboard("e")
        while not inserted:
            _,label = self.collect_process(phase, process)
            labels.append(label)
            print("predicted label is: ", label)
            
            pose = None
            if label == 'diagonal_2points':
                pose = 0
            elif label == "one_line":
                pose = 1
            elif label == "one_surface":
                pose = 2

            self.obs.append(pose)

            current = self.obs.get_observation() # format =[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
            print(current)
            current=np.array(current)
            print(current.shape)
            action = self.mlp_agant.act(current) # [0]   action=[0]   action[0]=0
            
            if pose == 2:
                inserted = True
                process = "in_hole"
                break
            
            word = self.robot_move(action[0])
            actions.append(word)
            print("this is action: ", word)

        print("found hole!")
        print(labels)
        print(actions)
        
        _,label = self.collect_process(phase, process)
        
    def collect_process(self, phase, process):
        time.sleep(1)
        z_before = self.get_current_z_coordinate()
        fail = 0
        label = None
        while True:
            self.action_publisher.get_keyboard('d')
            z_after = self.get_current_z_coordinate()
            z_distance = abs(z_before - z_after)
            
            print(f"Z distance traveled: {z_distance:.4f} m")
            print(z_distance)
            
            # if phase == 'z_phase':
            #     limit = 20000
            # elif phase == 'x_phase':
            #     limit = 24000
            # elif phase == 'hole_phase':
            #     limit = 35000
            # else:
            #     limit = 20000

            limit = 8000
            # print(limit)
                
            if z_distance > limit:
                # self.action_publisher.get_results()
                if process == "in_progress":
                    label = self.action_publisher.get_results().message
                    self.action_publisher.get_keyboard('u')
                else:
                    label = "Done"
                    time.sleep(1)
                    self.action_publisher.get_keyboard("o")
                break
            
            else:
                print("Z distance is too small; moving up and retrying...")
                self.action_publisher.get_keyboard('u')
                time.sleep(1)
                fail += 1
        
        time.sleep(1)
        return fail, label
            
    def demo_data_collect(self):
        msg = String()
        self.action_publisher.get_keyboard('i')
        self.action_publisher.get_keyboard('e')
        total_fail = 0
        fail_z = 0
        fail_x = 0
        fail_hole = 0
        fail_list = []
        process = "in_progress"

        #################################################### for outside of ideal trajectories ###########################################
        # z range: range(1, 11)
        # x range: range(0, 11), range(2, 11), range(3, 11), range(4, 11), range(5, 11), range(6, 11), range(7, 11), range(8, 11), range(9, 11)
        ######################################################################################################################################
        
        for i in range(1, 11):
            folder_name = f"/root/ur5/vibecheck_ws/classification/data/contact_type/2025-2-27/noisy_data/test_set/diagonal_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)
            phase = 'z_phase'        
            fail, _ = self.collect_process(phase, process)
            self.action_publisher.get_keyboard('z')
            fail_z += fail
            
        print('fail in z phase:', fail_z)
        
        for i in range(1, 11):
            folder_name = f"/root/ur5/vibecheck_ws/classification/data/contact_type/2025-2-27/noisy_data/test_set/one_line_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)
                    
            phase = 'x_phase'        
            fail, _ = self.collect_process(phase, process)
            self.action_publisher.get_keyboard('x')
            fail_x += fail
        print('fail in x phase:', fail_x)
            
        for i in range(1, 11):
            folder_name = f"/root/ur5/vibecheck_ws/classification/data/contact_type/2025-2-27/noisy_data/test_set/in_hole_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)

            phase = 'hole_phase'        
            fail, _ = self.collect_process(phase, process)
            fail_hole += fail
        print('fail in hole phase:', fail_hole)
        
        total_fail = fail_z + fail_x + fail_hole
        fail_list = [fail_z, fail_x, fail_hole]
        print('total fail:', total_fail)
        
        ##############################################################################################################################
        
        # for i in range(1, 11):
        #     self.action_publisher.get_keyboard('r')
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/contact_type/2025-2-27/twenty_random_sample_data/test_set/diagonal_out_of_distribution"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
        #     phase = 'z_phase'        
        #     fail, _ = self.collect_process(phase, process)
        #     fail_z += fail
            
        # print('fail in x phase:', fail_z)
        
        ####################################################################################################################################
        
        self.action_publisher.get_keyboard('i')
        self.action_publisher.get_keyboard('o')

    def test_model(self):
        labels = []
        process = "in_progress"
        self.action_publisher.get_keyboard('i')
        self.action_publisher.get_keyboard('r')
        for i in range(10):
            _, label = self.collect_process(process)
            
            pose = None
            if label == 'diagonal_2points':
                pose = 0
            elif label == "one_line":
                pose = 1
            elif label == "one_surface":
                pose = 2
                
            labels.append(pose)
            self.action_publisher.get_keyboard('u')
        
        print(labels)

    def material_grasppoing_internalstructure_estimation_task_data_collection(self):
        # self.action_publisher.get_keyboard('j')
        
        ########################################## material with different shape #########################################

        # msg = String()
        # folder_name = f"/root/ur5/vibecheck_ws/classification/data/material_classification/2025-2-22/test_set3/woo"
        # msg.data = folder_name
        # self.dir_pub.publish(msg)
        
        # for i in range(10):
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('g')
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('o')


        ########################################### grasping point ####################################################
        # self.action_publisher.get_keyboard('j')
        # msg = String()
        # folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set3/alu_edge"
        # msg.data = folder_name
        # self.dir_pub.publish(msg)
        
        
        # for i in range(5):
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('g')
            
        #     time.sleep(0.5)
        #     for i in range(5):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('o')
        
        ############################################ internal structure ###################################################

        ranges = [(1, 6), (6, 11), (11, 15), (15, 21)]
        start, end = ranges[0]
        print("it will loop from ", start, "to " , end)

        for i in range(1,20):
            msg = String()
            folder_name = f"/root/ur5/vibecheck_ws/classification/data/internal_structure/2025-2-28/test_set/cylinder_3/p{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)
            
            
            for i in range(1):
                time.sleep(0.1)
                self.action_publisher.get_keyboard('g')
                
                time.sleep(0.5)
                for i in range(1):
                    time.sleep(0.1)
                    self.action_publisher.get_keyboard('c')
                    
                time.sleep(0.1)
                self.action_publisher.get_keyboard('o')
                
            self.action_publisher.get_keyboard('n')

        # ranges = [(1, 6), (6, 11), (11, 15), (15, 21)]
        # start, end = ranges[0]
        # print("it will loop from ", start, "to " , end)

        # for i in range(1,21):
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/internal_structure/2025-2-28/test_set/cylinder_3/p{i}"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
            
        #     for i in range(5):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('g')
                
        #         time.sleep(0.5)
        #         for i in range(5):
        #             time.sleep(0.1)
        #             self.action_publisher.get_keyboard('c')
                    
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('o')
                
        #     self.action_publisher.get_keyboard('l')
        

        # msg = String()
        # folder_name = f"/root/ur5/vibecheck_ws/classification/data/internal_structure/2025-2-24/test_set/cylinder_2/p1"
        # msg.data = folder_name
        # self.dir_pub.publish(msg)
        
        
        # for i in range(10):
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('g')
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('o')
                
        
        ########################################## different orientation #########################################
        # self.action_publisher.get_keyboard('i')
        
        # for i in range(10):
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('g')
        #     time.sleep(0.5)
        #     self.action_publisher.get_keyboard('j')
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set4/alu_center"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
            
        #     self.action_publisher.get_keyboard('x')
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set5/alu_center"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
            
        #     self.action_publisher.get_keyboard('j')
        #     self.action_publisher.get_keyboard('m')
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set6/alu_center"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
            
        #     self.action_publisher.get_keyboard('j')
        #     self.action_publisher.get_keyboard(',')
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set7/alu_center"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
            
        #     self.action_publisher.get_keyboard('j')
        #     self.action_publisher.get_keyboard('.')
        #     msg = String()
        #     folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set8/alu_center"
        #     msg.data = folder_name
        #     self.dir_pub.publish(msg)
            
        #     time.sleep(0.5)
        #     for i in range(1):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
            
        #     self.action_publisher.get_keyboard('j')
        #     self.action_publisher.get_keyboard('i')
        #     self.action_publisher.get_keyboard('o')
        #     time.sleep(0.1)
            
        ########################################## different orientation (vertical) #########################################
        # self.action_publisher.get_keyboard('j')

            
        # msg = String()
        # folder_name = f"/root/ur5/vibecheck_ws/classification/data/grasping_point/2025-2-24/test_set4/woo_center"
        # msg.data = folder_name
        # self.dir_pub.publish(msg)
        
        # for i in range(5):
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('g')
            
        #     time.sleep(0.5)
        #     for i in range(5):
        #         time.sleep(0.1)
        #         self.action_publisher.get_keyboard('c')
                
        #     time.sleep(0.1)
        #     self.action_publisher.get_keyboard('o')
               
    def no_contact_analysis(self):
        self.action_publisher.get_keyboard('e')
        
        for i in range(1,11):
            msg = String()
            folder_name = f"/root/ur5/vibecheck_ws/data/feb_19_data/no_contact_analysis/test_set/diagonal_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)   

            time.sleep(0.5)
            label = self.action_publisher.get_results().message
            print(label)   
            self.action_publisher.get_keyboard("z")
                 
            
        for i in range(1, 11):
            folder_name = f"/root/ur5/vibecheck_ws/data/feb_19_data/no_contact_analysis/test_set/one_line_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)
                    
            time.sleep(0.5)
            label = self.action_publisher.get_results().message   
            print(label)
            self.action_publisher.get_keyboard('x')
            
        for i in range(1, 11):
            folder_name = f"/root/ur5/vibecheck_ws/data/feb_19_data/no_contact_analysis/test_set/in_hole_{i}"
            msg.data = folder_name
            self.dir_pub.publish(msg)
                    
            time.sleep(0.5)
            label = self.action_publisher.get_results().message   
            print(label)
#######################################################################################  
  
def main():
    rclpy.init()
    #sensor

    action_publisher = ActionPublisher(None)
    keyboard_input = KeyboardInput(action_publisher)
    action_publisher.keyboard_input = keyboard_input
    
    with keyboard_input as ki:
        try:
            rclpy.spin(action_publisher)
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    main()