# VLA Manipulation ROS 2

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?logo=ros)
![MoveIt 2](https://img.shields.io/badge/MoveIt_2-Enabled-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![C++](https://img.shields.io/badge/C++-17-blue?logo=c%2B%2B)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange)

Zero-Shot Language-Directed Pick & Place using ROS 2, MoveIt 2, and Vision-Language Models (VLMs).

## 🚀 Overview

This repository captures the state of an advanced **Vision-Language-Action (VLA)** pipeline designed for zero-shot robotic manipulation. It allows a 6-DOF robotic arm to perform complex pick-and-place operations based on natural language commands (e.g., *"Pick up the red block"*).

By integrating Vision-Language Models (VLMs) for zero-shot semantic reasoning with MoveIt 2 for collision-free motion planning, this architecture bridges the gap between Generative AI and classical deterministic robot control.

### Project Status

| Stage | Status | Evidence |
|---|---|---|
| **Perception Node (`vla_perception`)** | ✅ Complete | Parses `/camera/image_raw` and text prompts, generates 2D bounding boxes (currently using OpenCV color fallback for offline testing). |
| **Spatial Projection (`vla_spatial`)** | ✅ Complete | Uses `sensor_msgs_py` to extract 3D depth from `PointCloud2` at the bounding box center and publishes `tf2` target frames. |
| **MoveIt Execution (`vla_execution`)** | ✅ Complete | C++ node listens to `tf2`, generates `PoseStamped`, and queries MoveIt `MoveGroupInterface` for IK and trajectory planning. |
| **Simulation (`vla_gazebo`)** | ✅ Complete | Gazebo Classic world (`vla_world.sdf`) equipped with a table, target blocks, and a `libgazebo_ros_camera` RGB-D sensor. |
| **Pipeline Integration** | ✅ Complete | Unified `vla_pipeline.launch.py` boots Gazebo, camera drivers, TF broadcasters, and the full ROS 2 VLA autonomy stack simultaneously. |

---

## 🧠 System Architecture

The pipeline consists of four distinct ROS 2 packages operating in a closed loop:

1. **`vla_gazebo` (Environment)**
   * Spawns the physical simulation, the target objects, and the RGB-D camera.
   * Publishes `/camera/image_raw` and `/camera/points`.

2. **`vla_perception` (The Brain)**
   * Subscribes to the RGB image and `/vla/user_prompt`.
   * Processes the natural language command (simulated API delay).
   * Outputs a 2D bounding box JSON string to `/vla/target_bounding_box`.

3. **`vla_spatial` (The Bridge)**
   * Cross-references the 2D bounding box with the synchronized `PointCloud2` depth cloud.
   * Extracts real-world 3D coordinates (X, Y, Z).
   * Publishes spatial transforms to the ROS 2 `tf2` tree as `vla_target_<object>`.

4. **`vla_execution` (The Body)**
   * A C++ MoveIt 2 wrapper node that dynamically polls for the `vla_target_*` TF frame.
   * Computes Inverse Kinematics (IK) and executes a collision-free Cartesian trajectory via `MoveGroupInterface`.

---

## 🛠️ Installation & Setup

This package is built for **ROS 2 Humble / Jazzy**.

```bash
# 1. Clone the repository
cd ~/vla_manipulation_ros2

# 2. Build the workspace
colcon build --symlink-install

# 3. Source the environment
source install/setup.bash
```

## 🚀 Run Commands

To launch the entire simulation and VLA autonomy stack in one command:

```bash
ros2 launch vla_bringup vla_pipeline.launch.py
```

### Triggering the Robot

In a separate terminal, publish a natural language prompt to trigger the VLM and initiate the manipulation sequence:

```bash
ros2 topic pub --once /vla/user_prompt std_msgs/msg/String "{data: 'Pick up the red block'}"
```

Watch the terminal logs as the perception node detects the object, the spatial node calculates the depth, and the execution node plans the MoveIt trajectory!

---
*Developed by Paneendra Kumar*
