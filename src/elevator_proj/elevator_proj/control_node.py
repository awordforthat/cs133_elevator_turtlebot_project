from elevator_proj.constants import HRI_TOPIC, TEST_TOPIC, FEEDBACK_TOPIC
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ControlNode(Node):
    def __init__(self):
        super().__init__("control_node")
        self.publisher_ = self.create_publisher(String, HRI_TOPIC, 10)
        self.feedback_subscription = self.create_subscription(
            String, FEEDBACK_TOPIC, self.feedback_callback, 10
        )
        self.test_subscription = self.create_subscription(
            String, TEST_TOPIC, self.test_callback, 10
        )

    def test_callback(self, msg):
        self.publisher_.publish(msg)

    def feedback_callback(self, msg):
        self.get_logger().info(f"Control node got feedback: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    control_node = ControlNode()

    rclpy.spin(control_node)

    control_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
