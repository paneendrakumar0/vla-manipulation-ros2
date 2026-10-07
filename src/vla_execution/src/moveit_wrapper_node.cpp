#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>
#include <geometry_msgs/msg/pose_stamped.hpp>

class MoveItWrapperNode : public rclcpp::Node
{
public:
    MoveItWrapperNode() : Node("moveit_wrapper_node")
    {
        RCLCPP_INFO(this->get_logger(), "Initializing VLA MoveIt Execution Node...");

        tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
        tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
        
        // Timer to poll for the TF frame published by the spatial node
        timer_ = this->create_wall_timer(
            std::chrono::seconds(2),
            std::bind(&MoveItWrapperNode::check_for_target, this));
            
        RCLCPP_INFO(this->get_logger(), "Execution node ready. Waiting for target TF frames.");
    }

private:
    void check_for_target()
    {
        std::string target_frame = "vla_target_target"; // Mock frame from spatial_node
        std::string base_frame = "base_link"; // Assuming a standard robot base

        try {
            auto transform = tf_buffer_->lookupTransform(base_frame, target_frame, tf2::TimePointZero);
            
            RCLCPP_INFO(this->get_logger(), "Found target frame! Planning path...");
            plan_and_execute(transform);
            
            // Stop the timer to prevent infinite looping during development
            timer_->cancel();
        } catch (const tf2::TransformException & ex) {
            // Keep waiting silently
        }
    }

    void plan_and_execute(const geometry_msgs::msg::TransformStamped& target_transform)
    {
        // NOTE: In a real simulation, this node must be launched with the correct MoveIt parameters
        // For the sake of architecture setup, we log the intended action.
        
        geometry_msgs::msg::PoseStamped target_pose;
        target_pose.header.frame_id = target_transform.header.frame_id;
        target_pose.pose.position.x = target_transform.transform.translation.x;
        target_pose.pose.position.y = target_transform.transform.translation.y;
        target_pose.pose.position.z = target_transform.transform.translation.z;
        target_pose.pose.orientation = target_transform.transform.rotation;

        RCLCPP_INFO(this->get_logger(), "Target coordinates extracted. Initializing MoveGroupInterface...");
        
        using moveit::planning_interface::MoveGroupInterface;
        
        try {
            auto move_group = MoveGroupInterface(shared_from_this(), "manipulator");
            move_group.setPoseTarget(target_pose);

            MoveGroupInterface::Plan my_plan;
            bool success = (move_group.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);

            if (success) {
                RCLCPP_INFO(this->get_logger(), "Plan successful. Executing...");
                move_group.execute(my_plan);
            } else {
                RCLCPP_ERROR(this->get_logger(), "Planning failed!");
            }
        } catch (const std::exception& e) {
            RCLCPP_ERROR(this->get_logger(), "MoveGroupInterface initialization failed: %s", e.what());
        }
        
        RCLCPP_INFO(this->get_logger(), "Mock execution complete. Ready for next command.");
    }

    std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
    std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MoveItWrapperNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
