# VLA Manipulation ROS 2

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?logo=ros)
![MoveIt 2](https://img.shields.io/badge/MoveIt_2-Enabled-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![C++](https://img.shields.io/badge/C++-17-blue?logo=c%2B%2B)

Zero-Shot Language-Directed Pick & Place using ROS 2, MoveIt 2, and Vision-Language Models (VLMs).

## 🚀 Overview

This project bridges the gap between Generative AI and classical deterministic robot control. It allows a 6-DOF robotic arm to perform complex pick-and-place operations based on natural language commands (e.g., *"Pick up the red apple and put it in the bowl"*).

By integrating a Vision-Language Model (VLM) for zero-shot semantic reasoning with MoveIt 2 for collision-free motion planning, this architecture demonstrates a modern **Vision-Language-Action (VLA)** pipeline—a highly sought-after capability in modern robotics.

## 🧠 System Architecture

The system is divided into three core modules:

1. **The Brain (Perception & Semantic Reasoning)**
   * Captures RGB-D camera feeds from the simulated environment.
   * Processes natural language user prompts.
   * Uses a VLM to perform zero-shot object detection and outputs 2D bounding boxes of the target and destination.

2. **The Bridge (Spatial Mathematics & TF2)**
   * Cross-references the 2D bounding boxes with the depth cloud to extract real-world 3D coordinates.
   * Calculates required grasp orientations (quaternions).
   * Publishes spatial transforms to the ROS 2 `tf2` tree.

3. **The Body (Kinematics & Execution)**
   * A MoveIt 2 wrapper node that consumes the 3D target coordinates.
   * Computes Inverse Kinematics (IK) and collision-free Cartesian trajectories.
   * Executes the motion on the simulated robot arm.

## 🛠️ Tech Stack

* **Middleware:** ROS 2 (Humble)
* **Motion Planning:** MoveIt 2
* **Simulation:** Gazebo / Ignition
* **AI/Perception:** Vision-Language Models (API/Local), OpenCV, cv_bridge
* **Languages:** Python (Perception/AI), C++ (High-speed control nodes)

## 📂 Project Structure

\`\`\`text
vla_manipulation_ros2/
├── src/
│   ├── vla_perception/      # VLM integration and bounding box generation
│   ├── vla_spatial/         # Depth processing and tf2 broadcasting
│   ├── vla_moveit_config/   # Robot specific MoveIt configurations
│   └── vla_bringup/         # Launch files for the full pipeline
└── README.md
\`\`\`

## ⚙️ Setup & Installation

*(Instructions will be added as packages are developed)*

## 🚀 Usage

*(Usage instructions and prompt examples will be added here)*
