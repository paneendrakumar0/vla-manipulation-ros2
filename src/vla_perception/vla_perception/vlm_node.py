import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np

class VLMPerceptionNode(Node):
    def __init__(self):
        super().__init__('vlm_perception_node')
        self.get_logger().info("Initializing VLA Perception Node (VLM integration)...")
        
        self.bridge = CvBridge()
        
        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
            
        self.prompt_sub = self.create_subscription(
            String,
            '/vla/user_prompt',
            self.prompt_callback,
            10)
            
        # Publishers
        self.bbox_pub = self.create_publisher(String, '/vla/target_bounding_box', 10)
        
        self.latest_image = None
        self.current_prompt = None
        
        self.get_logger().info("VLM Node ready. Waiting for images and text prompts.")

    def image_callback(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")

    def prompt_callback(self, msg):
        self.current_prompt = msg.data
        self.get_logger().info(f"Received Command: '{self.current_prompt}'")
        self.process_vlm_request()
        
    def process_vlm_request(self):
        if self.latest_image is None:
            self.get_logger().warn("Cannot process prompt: No image received yet.")
            return
            
        self.get_logger().info("Sending image and prompt to Vision-Language Model...")
        
        # TODO: Integrate actual VLM API call (e.g., LLaVA, GPT-4o, Claude) here.
        # For scaffolding, we mock a bounding box response.
        mock_bbox = '{"object": "target", "x_min": 100, "y_min": 150, "x_max": 200, "y_max": 250}'
        
        msg = String()
        msg.data = mock_bbox
        self.bbox_pub.publish(msg)
        self.get_logger().info(f"Published Bounding Box: {mock_bbox}")

def main(args=None):
    rclpy.init(args=args)
    node = VLMPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
