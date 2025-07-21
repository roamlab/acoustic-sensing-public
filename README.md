# VibeCheck Keyboard Control

This repository contains the codebase for VibeCheck project. The system uses a UR5 robot arm equipped with a parallel gripper with piezo electric sensors used to classifiy contacts into one of three types: `diagonal_2points`, `one_line`, or `one_surface`.

## Directory Structure

```
vibecheck_ws/
├── README.md                
├── arduino_sketch/           # Arduino sketches for Teensy
├── build/                    
├── classification/           # Jupyter notebooks and scripts for analyzing model performance
│   ├── confusion_matrix.py
│   ├── data_analyst_classification.ipynb
├── full_requirements.txt     # Full list of Python packages (use for full environment recreation)
├── install/                  
├── log/                      
├── model/                    # Saved models used for classification (MLP and KPCA)
│   ├── MLP_train_demo_process_fixed_pca_parm_below_21000_02_28
│   ├── KPCA_train_demo_process_fixed_pca_parm_below_21000_02_28
├── nano/                     
├── plot/                     # Signal and frequency domain visualization scripts
│   ├── plot_fft.py
│   ├── plot_raw_signal.py
│   ├── plot_three_fft.py
│   ├── plot_three_fft_for_one_data.py
├── policy/                   # Trained MLP policy model(s)
│   ├── model_try-limit-init2027.pth
├── requirements.txt          # Minimal list of required Python dependencies
├── src/                      # ROS 2 package source files
│   └── keyboard_control/
│       ├── keyboard_control/ # Python implementation of ROS 2 nodes
│       │   ├── classifior.py      # FFT + KPCA + MLP classifier
│       │   ├── control.py         # Main service for coordinating classification and command
│       │   ├── data_collector.py  # Sensor data subscriber and logger
│       │   ├── fin_control.py     # Dynamixel gripper controller
│       │   ├── keyboard.py        # Keyboard interface for robot control
│       │   ├── MLP_policy.py      # Policy-based control using MLP model
│       │   ├── ur5_action.py      # UR5 motion primitives and contact-aware movements
│       ├── LICENSE
│       ├── package.xml
│       ├── setup.py, setup.cfg    
│       ├── resource/, test/       
```

Let me know if you'd like this merged into your README or saved to the file directly.

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

| Key | Action |
|-----|--------|
| `d` | Move down until contact |
| `u` | Move up |
| `z/x/n/m` | Rotate around z or x axes (forward/backward) |
| `i/e/j/r` | Move to predefined poses |
| `c` | Collect sensor data and classify contact |
| `g/o` | Close/Open gripper |
| `s` | Heuristic autonomous exploration |
| `p` | Auto data collection for contact type |
| `b` | Deploy trained MLP policy |
| `h` | Test MLP policy |
| `/` | Run material/grasp point/internal structure data collection task |

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
