import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped
import tf2_ros
import json
import math
import sensor_msgs_py.point_cloud2 as pc2

class SpatialTransformNode(Node):
    def __init__(self):
        super().__init__('spatial_transform_node')
        self.get_logger().info("Initializing VLA Spatial Node (2D BBox to 3D TF2)...")
        
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        self.bbox_sub = self.create_subscription(String, '/vla/target_bounding_box', self.bbox_callback, 10)
        self.pc_sub = self.create_subscription(PointCloud2, '/camera/points', self.pointcloud_callback, 10)
            
        self.latest_pointcloud = None

    def pointcloud_callback(self, msg):
        self.latest_pointcloud = msg

    def bbox_callback(self, msg):
        self.get_logger().info(f"Received BBox for projection: {msg.data}")
        try:
            bbox_data = json.loads(msg.data)
            self.project_to_3d(bbox_data)
        except Exception as e:
            self.get_logger().error(f"Failed to parse BBox JSON: {e}")
            
    def project_to_3d(self, bbox):
        if self.latest_pointcloud is None:
            self.get_logger().warn("Waiting for depth pointcloud...")
            return
            
        self.get_logger().info("Calculating 3D center of object from depth cloud...")
        
        # Calculate center of the bounding box
        center_x = int((bbox['x_min'] + bbox['x_max']) / 2)
        center_y = int((bbox['y_min'] + bbox['y_max']) / 2)
        
        # Extract the 3D point from the PointCloud2 at (center_x, center_y)
        # Assuming an organized point cloud (width, height)
        pc = self.latest_pointcloud
        if pc.height > 1:
            # Organized point cloud
            gen = pc2.read_points(pc, field_names=("x", "y", "z"), skip_nans=False, uvs=[[center_x, center_y]])
            point = next(gen, None)
        else:
            # Unorganized point cloud - we mock the logic since index matching requires camera intrinsics
            self.get_logger().warn("Unorganized point cloud detected. Mocking projection...")
            point = (1.0, 0.0, 0.2)
            
        if point is None or math.isnan(point[0]):
            self.get_logger().error("Valid depth point not found at bbox center.")
            return

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = pc.header.frame_id
        t.child_frame_id = f"vla_target_{bbox.get('object', 'item')}"
        
        t.transform.translation.x = float(point[0])
        t.transform.translation.y = float(point[1])
        t.transform.translation.z = float(point[2])
        
        # Grasp orientation points straight down as a baseline
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.7071
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 0.7071
        
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info(f"Published TF frame {t.child_frame_id} at XYZ: ({point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f})")

def main(args=None):
    rclpy.init(args=args)
    node = SpatialTransformNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
