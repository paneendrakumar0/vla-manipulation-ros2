import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
import json
import time

class VLMPerceptionNode(Node):
    def __init__(self):
        super().__init__('vlm_perception_node')
        self.get_logger().info("Initializing VLA Perception Node...")
        
        self.bridge = CvBridge()
        
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.prompt_sub = self.create_subscription(String, '/vla/user_prompt', self.prompt_callback, 10)
        self.bbox_pub = self.create_publisher(String, '/vla/target_bounding_box', 10)
        
        self.latest_image = None
        
        self.get_logger().info("VLM Node ready. Waiting for prompts...")

    def image_callback(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")

    def prompt_callback(self, msg):
        prompt = msg.data.lower()
        self.get_logger().info(f"Received VLA Command: '{prompt}'")
        
        if self.latest_image is None:
            self.get_logger().warn("No image received yet. Cannot process prompt.")
            return
            
        # Simulating a VLM inference delay
        self.get_logger().info("Sending image and prompt to Vision-Language Model API...")
        time.sleep(1.5) 
        
        # In a production environment, this calls google-genai or openai.
        # For this stage, we implement a robust OpenCV color fallback to allow closed-loop testing.
        target_color = None
        if 'red' in prompt: target_color = 'red'
        elif 'blue' in prompt: target_color = 'blue'
        elif 'green' in prompt: target_color = 'green'
        
        if target_color:
            bbox = self.detect_color(self.latest_image, target_color)
            if bbox:
                response = {
                    "object": target_color,
                    "x_min": int(bbox[0]), "y_min": int(bbox[1]),
                    "x_max": int(bbox[0] + bbox[2]), "y_max": int(bbox[1] + bbox[3])
                }
                self.bbox_pub.publish(String(data=json.dumps(response)))
                self.get_logger().info(f"VLM Detected Object: {response}")
            else:
                self.get_logger().warn(f"VLM failed to locate '{target_color}' in the current frame.")
        else:
            self.get_logger().warn("Prompt not understood by mock VLM. Try 'Pick up the red block'.")

    def detect_color(self, img, color):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if color == 'red':
            mask1 = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
            mask = mask1 + mask2
        elif color == 'blue':
            mask = cv2.inRange(hsv, np.array([100, 150, 0]), np.array([140, 255, 255]))
        elif color == 'green':
            mask = cv2.inRange(hsv, np.array([36, 25, 25]), np.array([86, 255, 255]))
        else:
            return None

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 100:
                return cv2.boundingRect(largest)
        return None

def main(args=None):
    rclpy.init(args=args)
    node = VLMPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
