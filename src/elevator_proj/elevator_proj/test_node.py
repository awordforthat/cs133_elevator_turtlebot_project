
import threading 

from elevator_proj.constants import TEST_TOPIC
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TestNode(Node):
    def __init__(self):
        super().__init__("test_node")
        self.publisher_ = self.create_publisher(String, TEST_TOPIC, 10)
        threading.Thread(target=self.check_keyboard_input, daemon=True).start()

    def check_keyboard_input(self):
        while rclpy.ok():
            keyboard_input = input("Enter a command:")
            msg = String()
            msg.data = keyboard_input
            print("publishing", msg.data)
            self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    test_node = TestNode()

    rclpy.spin(test_node)

    test_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
        