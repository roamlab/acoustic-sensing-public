######################################

# !/usr/bin/python3

import rtde_control # real time communication with robot
import rtde_receive
import numpy as np
import transforms3d as tf
from scipy.spatial.transform import Rotation as R
import time
import math
import random
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Bool, Int16MultiArray
from example_interfaces.srv import AddTwoInts

class ContactDetection(Node):
    def __init__(self):
        super().__init__('minimal_service')
        
        self.subscription = self.create_subscription(
        Bool,
        'contact_detected',
        self.contact_callback,
        10
        )
        
        self.contact_flag=False
        
    def contact_callback(self, msg):
        """Callback function for the contact detection topic."""
        self.get_logger().info(f"Contact detected: {msg.data}")
        self.contact_flag=True
        print('get contact in model')
        
    def reset_flag(self):
      self.contact_flag=False
      
    def get_flag(self):
      return self.contact_flag
    
class EEPrimitives(Node):

  def __init__(self, exp, contact_model):
    super().__init__('ee_primitives_node')
    self.robot_ip = '192.168.0.216'

    self.publisher = self.create_publisher(Bool, 'contact_flag', 10)

    self.srv = self.create_service(AddTwoInts, 'ur5_control', self.action_translator)

    self.step = -0.005
    self.pose = exp
    
    self.speedJ = 0.5  # m/s
    self.accelJ = 0.3  # m/s^2
    self.speedL = 0.5  # m/s
    self.accelL = 0.1  # m/s^2
    self.speedD = 0.01  # m/s
    self.accelD = 0.1  # m/s^2

    self.rtde_c = rtde_control.RTDEControlInterface(self.robot_ip)
    self.rtde_r = rtde_receive.RTDEReceiveInterface(self.robot_ip)
    
    self.tcp_offset = [0, 0, 0.22, 0, 0, np.pi/2]
    self.rtde_c.setTcp(self.tcp_offset)
    self.tcp_pose = self.rtde_r.getActualTCPPose()

    self.threshhold_z = 0.05

    self.task_done = False

    self.contact_model=contact_model
    
    self.angle_z = (90-45)/10 # 52.97988511773741/10, 10
    self.angle_x = (180-135)/10 # 44.99015439026178/10
    self.angle_y = 45
    
    self.previous_angles = set()
  
  def action_translator(self, request, response):
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -122, 1, 35]
    pose = self.rtde_r.getActualTCPPose()
    print('get action')
    if request.a == 1:
      self.continuous_move_down(pose)
      response.sum=0
    elif request.a == 2:
      self.continuous_move_up(pose)
      response.sum=0
    elif request.a == 3:
      self.rotation_z_axis_forward(pose)
      response.sum=0
    elif request.a == 4:
      self.rotation_x_axis_forward(pose)
      response.sum=0
    elif request.a == 5:
      self.rotation_z_axis_backward(pose)
      response.sum=0
    elif request.a == 6:
      self.rotation_x_axis_backward(pose)
      response.sum=0
    elif request.a == 7:
      self.move_to_initial_pose()
      response.sum=0
    elif request.a == 8:
      euler_pose = self.computes_pose()
      z_in_meters = euler_pose[2]
      z_in_mm = z_in_meters * 1000000.0 
      response.sum = int(z_in_mm)
    elif request.a == 9:
      euler_pose = self.computes_pose_in_degree()
      response.sum=0 
    elif request.a == 10:
      self.move_to_random_initial_pose()
      response.sum=0
    elif request.a == 11:
      self.move_to_initial_pose_to_collect_data()
      response.sum=0
    elif request.a == 12:
      self.move_to_initial_pose_for_material_grasp_internal_task()
      response.sum=0
    elif request.a == 13:
      self.rotation_y_axis_forward(pose)
      response.sum=0
    elif request.a == 14:
      self.rotation_y_axis_backward(pose)
      response.sum=0
    elif request.a == 15:
      self.rotation_z_axis_random(pose)
    return response

  def euler_to_rotvec_pose(self, pose):
    axes, angle = tf.euler.euler2axangle(math.radians(pose[3]), math.radians(pose[4]), math.radians(pose[5]))
    rotvec = axes * angle
    pose[3:] = rotvec
    return pose

  def move_j_to_start(self, pose):
      """ Move to start joint pose """
      print('Moving to initial joint pose: ', pose)
      self.rtde_c.moveJ(pose, self.speedJ, self.accelJ)
      print('At start pose')

  def move_l_to_start(self, pose):
    """ move to start pose for experiments  """
    print('moving to start pose: ', pose)
    self.rtde_c.moveL(pose, self.speedL, self.accelL)
    print('at the pose for experiment!')
    
  def get_current_tcp_pose(self):
    # Get the current TCP pose
    current_tcp_pose = self.tcp_pose
    print("Current TCP Pose:", current_tcp_pose)
    return current_tcp_pose
  
  def computes_pose(self):
      """
      Computes the current TCP pose in Euler angles (in degrees).
      The returned pose is [x, y, z, roll, pitch, yaw], where
      x, y, z are in meters and roll, pitch, yaw are in degrees.
      """
      # The raw pose from the robot is [x, y, z, rx, ry, rz],
      # where rx, ry, rz is the axis-angle representation.
      tcp_pose = self.rtde_r.getActualTCPPose()  # e.g. [x, y, z, rx, ry, rz]
      x, y, z, rx, ry, rz = tcp_pose

      # Compute the angle (magnitude of the rotation vector).
      angle = math.sqrt(rx**2 + ry**2 + rz**2)

      if angle < 1e-10:
          # If the angle is near zero, there is effectively no rotation.
          # Euler angles in this case can be taken as [0, 0, 0].
          euler_rad = (0.0, 0.0, 0.0)
      else:
          # Normalize the axis vector
          axis = [rx / angle, ry / angle, rz / angle]
          # Convert axis-angle (in radians) to Euler angles (in radians)
          euler_rad = tf.euler.axangle2euler(axis, angle, axes='sxyz')

      # Convert from radians to degrees
      roll_deg, pitch_deg, yaw_deg = [math.degrees(a) for a in euler_rad]
      euler_pose = [x, y, z, roll_deg, pitch_deg, yaw_deg]

      # self.get_logger().info(f"TCP Pose in Euler (degrees): {euler_pose}")
      return euler_pose

  def computes_pose_in_degree(self):
      tcp_pose = self.rtde_r.getActualTCPPose()  # e.g. [x, y, z, rx, ry, rz]
      x, y, z, rx, ry, rz = tcp_pose


      angle = math.sqrt(rx**2 + ry**2 + rz**2)

      if angle < 1e-10:
          euler_rad = (0.0, 0.0, 0.0)
      else:
          axis = [rx / angle, ry / angle, rz / angle]
          euler_rad = tf.euler.axangle2euler(axis, angle, axes='sxyz')

      roll_deg, pitch_deg, yaw_deg = [math.degrees(a) for a in euler_rad]
      exp = [x, y, z, roll_deg, pitch_deg, yaw_deg]

      print("input exp is: ",exp)
      euler_pose_in_degree = exp

      return euler_pose_in_degree
    
  def move_to_initial_pose(self):
    ######################## initial pose setting ##################################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.05188298887537103, -122, 1, 35] 
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 1, 35] 
    ########################## various initial pose ################################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 45] 
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, 135, 0, 45] 
    ########################## various initial pose (changing platform) #########################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 45] # case 1: positive z, negative x
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, -45] # case 2: negative z, positive x
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 135] # case 3: negative z, negative x
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 225] # case 4: positive z, negative x - not sure yet?????
    #############################################################################################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 225] 
    # exp = [-0.5914156254820065, -0.09371589518438497, -0.08188298887537103, -135, 0, 135] 
    ########################### To collect data for whole workspace ###########################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 45] 
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-139.5, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-144, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-148.5, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-153, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-157.5, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-162, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-166.5, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-171, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-175.5, 0, 45]
    #       [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103,-180, 0, 45]
    ######################### for different orientation task ##################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.16808298887537103, -180, 0, 180] 
    ###########################################################################################
    
    exp = [-0.5944156254820065, -0.09571589518438497, -0.09588298887537103, -180, 0, 90] 
    current_angle = exp[3:]
    print("current initial pose is:", current_angle)
    pose = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(pose, self.speedL, self.accelL)
    return exp
  
  def move_to_initial_pose_for_material_grasp_internal_task(self):
    ########################################## internal structure ########################################3
    exp = [-0.5944156254820065, -0.09571589518438497, -0.16088298887537103, -180, 0, 180] 
    #####################################################################################################3
    
    ######################################### material classification #################################3
    
    ########################################### on the table ###########################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.16808298887537103, -180, 0, 180] 
    
    ########################################### on the acrylic board ######################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.162008298887537103, -180, 0, 180] 
    
    ###########################################3 on the textbook #######################################
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.132008298887537103, -180, 0, 180] 
    
    ############################################ on the plastic box ####################################3
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.0042008298887537103, -180, 0, 180] 
    
    ############################################ different orientation ####################################3
    # exp = [-0.5944156254820065, -0.09571589518438497, -0.0042008298887537103, -180, 0, 180] 
    
    ############################################ different orientation (horizontal) ####################################3
    
    # poses = [
    #           [-0.5944156254820065, -0.09571589518438497, -0.0042008298887537103, -90, -90, -180],
    #           [-0.5944156254820065, -0.09571589518438497, 0.0160708298887537103, -90, -90, -180],
    #           [-0.5944156254820065, -0.09571589518438497, 0.0463408298887537103, -90, -90, -180],
    #         ]
    # exp = poses[0]
    
    ###################################################################################################

    ###################################### banana ####################################################
    # exp = [-0.5944156254820065, -0.09571589518438497, 0.15088298887537103, -180, 0, 180] 
    
    current_angle = exp[3:]
    print("current initial pose is:", current_angle)
    pose = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(pose, self.speedL, self.accelL)
    return exp
  
  def move_to_initial_pose_to_collect_data(self):
    poses = [
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 45] ,
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -139.5, 0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -144,    0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -148.5,  0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -153,    0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -157.5,  0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -162,    0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -166.5,  0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -171,    0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -175.5,  0, 45],
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -180, 0, 90], 
        # [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -135, 0, 45]
        
        ############################### To collect data out of trajectory ####################################
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -130.5, 0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.09588298887537103, -135, 0, 45], ############### ideal trajectory
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -139.5, 0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -144,    0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -148.5,  0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -153,    0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -157.5,  0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -162,    0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -166.5,  0, 45],
        [-0.5944156254820065, -0.09571589518438497, -0.08188298887537103, -171,    0, 45]
        ###################################################################################################
    ]
    
    exp = poses[1]
    
    current_angle = exp[3:]
    print("current initial pose is:", current_angle)
    pose = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(pose, self.speedL, self.accelL)
    return exp
  
  def move_to_random_initial_pose(self):
    x_angles = np.linspace(-171, -130.5)
    z_angles = np.linspace(9, 90)
    x_angle = random.choice(x_angles)
    z_angle = random.choice(z_angles)
    exp = [-0.5944156254820065, -0.09571589518438497, -0.09588298887537103, x_angle, 0, z_angle]
    current_angle = exp[3:]
    print("current initial pose is:", current_angle)
    pose = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(pose, self.speedL, self.accelL)
    return exp

  def continuous_move_down(self,exp):
    """Move down incrementally along the z-axis."""
    self.action_done=False
    exp[2] -= 0.03    # Set the limit to protect the grippers
    self.contact_model.reset_flag()
    ####################for sending contact flag to teensy#####################
    msg = Bool()
    msg.data = True
    self.publisher.publish(msg)
    ###########################################################################
    self.rtde_c.moveL(exp, self.speedD, self.accelD, asynchronous= True)
    
    # time.sleep(2.5)        # for in_hole data collection,  also we can comment the following code out
    
    start_time = time.time()  # Record the start time
    timeout = 2.8  # Set the timeout to 3 seconds
    
    while not self.contact_model.get_flag():
        if time.time() - start_time > timeout:  # Check if the timeout has been exceeded
            print("Timeout exceeded, exiting loop.")
            break
        time.sleep(0.01)

    self.rtde_c.stopL()
    return exp

  def continuous_move_up(self,exp):
    """Move down incrementally along the z-axis."""

    exp[2] = -0.09588298887537103    # Set the limit to protect the grippers

    self.rtde_c.moveL(exp, self.speedL, self.accelL, asynchronous= True)

    return exp

  def rotation_z_axis_forward(self,exp):
    # Extract position and rotation
    x_pose, y_pose, z_pose = exp[:3]
    x_rot, y_rot, z_rot = exp[3:]
    
    # Compute the axis and angle
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5  # Angle is the magnitude of the axis vector
    axis = [x / theta for x in axis]  # Normalize axis

    # Convert axis-angle to Euler angles
    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]

    exp[5] += self.angle_z # 3 points: 17.666666666666666667 6 points: 8.8333333333333333333 # total angle: 53

    current_angle = exp[3:]    
    exp = self.euler_to_rotvec_pose(exp) 
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    print("current pose is:", current_angle)
    return exp  
  
  def rotation_z_axis_backward(self,exp):
    x_rot, y_rot, z_rot = exp[3:]
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
    axis = [x / theta for x in axis]

    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
    print("converted to degrees:",exp)
    
    exp[5] -= self.angle_z # 3 points: 17.666666666666666667 6 points: 8.8333333333333333333

    current_angle = exp[3:]
    exp = self.euler_to_rotvec_pose(exp)  
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    print("current pose is:", current_angle)  
    return exp  
  
  def rotation_z_axis_random(self, exp):
      if not hasattr(self, "previous_angles"):
          self.previous_angles = set()

      x_rot, y_rot, z_rot = exp[3:]
      axis = [x_rot, y_rot, z_rot]
      theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
      axis = [x / theta for x in axis]

      euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
      exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
      print("Converted to degrees:", exp)
      
      while True:
          random_angle = random.uniform(0, 180)
          if random_angle not in self.previous_angles:
              self.previous_angles.add(random_angle)
              break
      
      exp[5] = random_angle
      current_angle = exp[3:]
      print(f"Current pose is: {current_angle}, Random Z-angle applied: {random_angle}")
      exp = self.euler_to_rotvec_pose(exp)
      self.rtde_c.moveL(exp, self.speedL, self.accelL) 

      return exp

  def rotation_x_axis_forward(self,exp):
    x_rot, y_rot, z_rot = exp[3:]
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
    axis = [x / theta for x in axis]

    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
    print("converted to degrees:",exp)
    
    exp[3] -= self.angle_x # 3 points: 15 6 points: 7.5, exp[3] -= 6.66666666666666666667 # 13.333333333333333333 # total angle: 45
    current_angle = exp[3:]
    print("current pose is:", current_angle)
    exp = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    return exp  
  
  def rotation_x_axis_backward(self,exp):
    x_rot, y_rot, z_rot = exp[3:]
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
    axis = [x / theta for x in axis]

    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
    print("converted to degrees:",exp)

    exp[3] += self.angle_x # 3 points: 15 6 points: 7.5, exp[3] -= 6.66666666666666666667 # 13.333333333333333333
    current_angle = exp[3:]
    print("current pose is:", current_angle)      
    exp = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    return exp  
  
  def rotation_y_axis_forward(self,exp):
    x_rot, y_rot, z_rot = exp[3:]
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
    axis = [x / theta for x in axis]

    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
    print("converted to degrees:",exp)
    
    exp[4] += self.angle_y
    current_angle = exp[3:]
    print("current pose is:", current_angle)    
    exp = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    return exp  
  
  def rotation_y_axis_backward(self,exp):
    x_rot, y_rot, z_rot = exp[3:]
    axis = [x_rot, y_rot, z_rot]
    theta = (x_rot**2 + y_rot**2 + z_rot**2) ** 0.5
    axis = [x / theta for x in axis]

    euler_angles = tf.euler.axangle2euler(axis, theta, axes='sxyz')
    exp[3:] = [math.degrees(euler_angles[0]), math.degrees(euler_angles[1]), math.degrees(euler_angles[2])]
    print("converted to degrees:",exp)
    
    exp[4] -= self.angle_y # 3 points: 17.666666666666666667 6 points: 8.8333333333333333333
    current_angle = exp[3:]
    print("current pose is:", current_angle)    
    exp = self.euler_to_rotvec_pose(exp)
    self.rtde_c.moveL(exp, self.speedL, self.accelL) 
    return exp

  def disconnect(self):
    self.get_logger().info('Disconnecting from robot.')
    self.rtde_c.stopScript()

def main(args=None):
    rclpy.init(args=args)
    exp = [-0.5944156254820065, -0.09571589518438497, -0.05188298887537103, -122, 1, 35] 
    contact_model=ContactDetection()
    EE = EEPrimitives(exp,contact_model)
    
    # pose = EE.euler_to_rotvec_pose(exp)
    # EE.move_l_to_start(pose)
    
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(EE)
    executor.add_node(contact_model)
    
    executor.spin()

            
    EE.disconnect()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

