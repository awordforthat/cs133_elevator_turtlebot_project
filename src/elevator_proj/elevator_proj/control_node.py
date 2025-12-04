from elevator_proj.constants import (
    AUDIO_CONTROL_START,
    FEEDBACK_SUCCESS,
    HRI_TOPIC,
    TEST_TOPIC,
    FEEDBACK_TOPIC,
)
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ControlNode(Node):
    def __init__(self):
        super().__init__("control_node")
        self.hri_publisher_ = self.create_publisher(String, HRI_TOPIC, 10)
        # self.recording_publisher = self.create_publisher(String, AUDIO_RECORD_TOPIC, 10)

        self.feedback_subscription = self.create_subscription(
            String, FEEDBACK_TOPIC, self.feedback_callback, 10
        )

        # TODO(echarles): replace with subscription to joystick controls
        self.test_subscription = self.create_subscription(
            String, TEST_TOPIC, self.test_callback, 10
        )

    def test_callback(self, msg):
        self.hri_publisher_.publish(msg)

    def feedback_callback(self, msg):
        self.get_logger().info(f"Control node got feedback: {msg.data}")
        if FEEDBACK_SUCCESS in msg.data:
            recording_message = String()
            recording_message.data = AUDIO_CONTROL_START
            # self.recording_publisher.publish()


def main(args=None):
    rclpy.init(args=args)
    control_node = ControlNode()

    rclpy.spin(control_node)

    control_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
