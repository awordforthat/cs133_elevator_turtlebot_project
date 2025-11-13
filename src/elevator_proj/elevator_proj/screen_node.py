
from elevator_proj.constants import HRI_TOPIC
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ScreenNode(Node):
    def __init__(self):
        super().__init__("screen_node")
        self.subscription = self.create_subscription(
            String,
            HRI_TOPIC,
            self.callback,
            10
        )
    

    def callback(self, msg):
        self.get_logger().info(f"Screen node heard: {msg.data}")


def main(args=None):
    rclpy.init(args=args)

    speech_node = ScreenNode()

    rclpy.spin(speech_node)

    speech_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()