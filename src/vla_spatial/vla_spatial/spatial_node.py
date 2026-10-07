import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped
import tf2_ros
import json

class SpatialTransformNode(Node):
    def __init__(self):
        super().__init__('spatial_transform_node')
        self.get_logger().info("Initializing VLA Spatial Node (3D Projection)...")
        
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        self.bbox_sub = self.create_subscription(
            String,
            '/vla/target_bounding_box',
            self.bbox_callback,
            10)
            
        self.pc_sub = self.create_subscription(
            PointCloud2,
            '/camera/points',
            self.pointcloud_callback,
            10)
            
        self.latest_pointcloud = None

    def pointcloud_callback(self, msg):
        self.latest_pointcloud = msg

    def bbox_callback(self, msg):
        self.get_logger().info(f"Received BBox for spatial transform: {msg.data}")
        
        try:
            bbox_data = json.loads(msg.data)
            self.project_to_3d(bbox_data)
        except Exception as e:
            self.get_logger().error(f"Failed to parse BBox: {e}")
            
    def project_to_3d(self, bbox):
        if self.latest_pointcloud is None:
            self.get_logger().warn("Waiting for point cloud data...")
            return
            
        self.get_logger().info("Calculating 3D center of object...")
        
        # TODO: Implement pointcloud projection logic
        # For now, we mock the output transform
        t = TransformStamped()
        
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'camera_link'
        t.child_frame_id = f"vla_target_{bbox.get('object', 'item')}"
        
        t.transform.translation.x = 0.5
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.2
        
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info(f"Published TF frame: {t.child_frame_id}")

def main(args=None):
    rclpy.init(args=args)
    node = SpatialTransformNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
