# VibeCheck: Using Active Acoustic Tactile Sensing for Contact-Rich Manipulation

<h1 align="center">
  <br>
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="image/logo.png" alt="Markdownify" width="200"></a>
  <br>
  VibeCheck
  <br>
</h1>

<h4 align="center"> A new kind of sensor usage.</h4>


<p align="center">
  <a href="#directory-structure">Directory Structure</a> •
  <a href="#system-overview">System Overview</a> •
  <a href="#keyboard-commands">Keyboard Commands</a> •
  <a href="#getting-started">Getting Started</a>
</p>

This repository contains the codebase for VibeCheck project. The system uses a UR5 robot arm equipped with a parallel gripper with piezo electric sensors used to classifiy contacts into one of three types: `diagonal_2points`, `one_line`, or `one_surface`.

## Directory Structure

```
VibeCheck/
├── README.md
├── classification/            # Jupyter notebooks and scripts for model training and evaluation
│   ├── MLP_training.ipynb             # Training pipeline for MLP classifier
│   ├── data_analyst_classification.ipynb
│   ├── data_analyst_classification_wilson.ipynb
│   ├── data_analyst_regression.ipynb
│   ├── visualize_the_rl_result.ipynb  # Visual summaries of RL performance
│   ├── confusion_matrix.py            # Utility script to visualize classification results
├── full_requirements.txt      # Full dependency list
├── requirements.txt           
├── image/
│   └── logo.png               
├── model/                     # Pretrained models for inference (used in keyboard interface)
│   ├── KPCA_train_demo_process_fixed_pca_parm_below_21000_02_28
│   └── MLP_train_demo_process_fixed_pca_parm_below_21000_02_28
├── plot/                      # Signal and FFT plotting utilities
│   ├── plot_fft.py
│   ├── plot_raw_signal.py
│   ├── plot_three_fft.py
│   └── plot_three_fft_for_one_data.py
├── policy/                    # Policy learning code (IL and RL) for autonomous exploration
│   ├── MLP.py                         # MLP-based imitation learning agent
│   ├── MLP_template.py               # Template script for MLP usage with robot interface
│   ├── IL_collect_data.py           # Collect IL data from simulated environment
│   ├── DQN_main.py                  # DQN-based reinforcement learning agent
│   ├── model_try-limit-init2027.pth # Pretrained MLP policy weights
│   ├── ENV/
│   │   └── env.py                   # Simulated environment for learning-based agents
│   └── model/
│       ├── DQN.py                   # Deep Q-Network and agent implementation
│       ├── ReplayMemory.py         # Experience replay buffer
│       └── utils.py                # Utility functions (e.g., soft update for target network)
├── src/
│   └── keyboard_control/           # ROS2 Python package
│       ├── keyboard_control/       
│       │   ├── classifior.py       # MLP+KPCA contact classifier (FFT-based)
│       │   ├── control.py          # Triggers classification + commands robot
│       │   ├── data_collector.py   # Collects sensor data from micro-ROS (Teensy)
│       │   ├── fin_control.py      # Gripper control via Dynamixel SDK
│       │   ├── keyboard.py         # Keyboard interface to deploy policy
│       │   ├── MLP_policy.py       # Loads and applies trained MLP policy
│       │   └── ur5_action.py       # Low-level control of the UR5 arm (RTDE)
│       ├── LICENSE
│       ├── package.xml             
│       ├── setup.py, setup.cfg     
│       ├── resource/, test/        
```

## System Overview
The pipeline is composed of several key modules:
- `keyboard.py`: The main keyboard controller, allowing manual triggering of robot movements, data collection, classification, and policy deployment.
- `data_collector.py`: Listens to micro-ROS messages from a Teensy-based sensor and optionally logs them to CSV.
- `control.py`: Coordinates data recording and invokes the classifier.
- `classifior.py`: A classifier that applies FFT, dimensionality reduction (KPCA), and then predicts with an MLP.
- `MLP_policy.py`: Loads a trained policy for imitation learning-based manipulation.
- `fin_control.py`: Dynamixel servo motor control (open/close gripper).
- `ur5_action.py`: Handles actual robot movements like going down until contact, rotations, and pose initialization.

## Keyboard Commands

You can control the robot via various key presses:

### Basic Motion Commands

| Key  | Action                                                |
|------|-------------------------------------------------------|
| `d`  | Move down until contact detection                     |
| `u`  | Move up                                               |
| `z`  | Rotate along Z-axis (forward / positive angle)        |
| `n`  | Rotate along Z-axis (backward / negative angle)       |
| `x`  | Rotate along X-axis (forward / positive angle)        |
| `m`  | Rotate along X-axis (backward / negative angle)       |
| `,`  | Rotate along Y-axis (forward / positive angle)        |
| `.`  | Rotate along Y-axis (backward / negative angle)       |
| `l`  | Assign random Z-axis rotation                         |

### Pose Management

| Key  | Action                                                             |
|------|--------------------------------------------------------------------|
| `i`  | Move to default initial pose                                       |
| `r`  | Move to a random initial pose                                      |
| `e`  | Move to pose to collect data                           	    |
| `j`  | Move to pose for specific tasks (e.g., material grasp/internal)    |

### Pose Calculation

| Key  | Action                                       |
|------|----------------------------------------------|
| `a`  | Compute Z pose in millimeters   	      |
| `t`  | Compute full Euler pose `[x,y,z]` in degrees |

### Sensing & Actuation

| Key  | Action                                    |
|------|-------------------------------------------|
| `c`  | Collect sensor data and classify label    |
| `g`  | Close the gripper                         |
| `o`  | Open the gripper                          |

### Autonomous Routines

| Key  | Action                                                                          |
|------|---------------------------------------------------------------------------------|
| `p`  | Auto data collection routine for peg-in-hole task                               |
| `/`  | Collect data for material properties, grasping point, and internal structure    |
| `s`  | Run heuristic-based exploration demo with adaptive contact classification       |
| `b`  | Deploy trained MLP policy for learned manipulation                              |
| `h`  | Test MLP model and print prediction results                                     |


## Getting Started

### 1. Requirements

All Python and ROS2 dependencies are listed in:

- `requirements.txt` – Python packages (minimal)
- `full_requirements.txt` – Full Python environment snapshot (recommended)

To install dependencies:
```bash
pip install -r full_requirements.txt
```

Make sure your environment also includes:
- ROS 2 Humble
- `rclpy`, `std_msgs`, `example_interfaces`
- Dynamixel SDK
- Pynput
- NumPy, Pandas, SciPy, Scikit-learn, PyTorch

---

### 2. Setup Environment and Build

```bash
# Source ROS2
source /opt/ros/humble/setup.bash
echo "sourced ROS2 Humble Hawksbill"

# Navigate to workspace and build
cd /root/ur5/vibecheck_ws
colcon build
source install/setup.bash
```

---

### 3. Aliases for Quick Use

Add the following to your `~/.bashrc` or execute them directly in your terminal for convenience:

```bash
# Micro-ROS Agent (one is for receiver and the other is for speaker)
alias agent0='cd /root/ur5/microros_ws && source install/setup.bash && echo "sourced microros_ws" && ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0'
alias agent1='cd /root/ur5/microros_ws && source install/setup.bash && echo "sourced microros_ws" && ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM1'

# ROS2 Humble
alias humble='source /opt/ros/humble/setup.bash && echo "sourced ROS2 Humble Hawksbill"'

# Run core nodes
alias data='cd /root/ur5/vibecheck_ws/src/keyboard_control/keyboard_control && python3 data_collector.py'
alias control='cd /root/ur5/vibecheck_ws/src/keyboard_control/keyboard_control && python3 control.py'
alias ur5_action='cd /root/ur5/vibecheck_ws/src/keyboard_control/keyboard_control && python3 ur5_action.py'
alias keyboard='cd /root/ur5/vibecheck_ws/src/keyboard_control/keyboard_control && python3 keyboard.py'
```

---

### 4. Run Nodes

Start your system in separate terminals:

```bash
# Terminal 1: Start micro-ROS agent (for receiver)
agent0

# Terminal 2: Start micro-ROS agent (for speaker)
agent1

# Terminal 3:
data

# Terminal 4:
control

# Terminal 5:
ur5_action

# Terminal 6:
keyboard
```
