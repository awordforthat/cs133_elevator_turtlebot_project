import time

from elevator_proj.constants import HRI_TOPIC, FEEDBACK_TOPIC
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SpeechNode(Node):
    def __init__(self):
        super().__init__("speech_node")
        self.subscription = self.create_subscription(
            String,
            HRI_TOPIC,
            self.callback,
            10
        )
        self.feedback_publisher_ = self.create_publisher(String,
                                                FEEDBACK_TOPIC, 10)

    def callback(self, msg):
        #TODO(echarles): figure out QoS so messages that come in during the 
        # speaking phase don't interrupt the speech. Maybe we want a "cancel" behavior?
        self.get_logger().info(f"Speech node heard: {msg.data}")
        i = 3
        while i > 0:
            self.get_logger().info(f"Waiting... {i}")
            time.sleep(1)
            i -= 1
        feedback = String()
        feedback.data = "Done"
        self.feedback_publisher_.publish(feedback)

def main(args=None):
    rclpy.init(args=args)

    speech_node = SpeechNode()

    rclpy.spin(speech_node)

    speech_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()