import rclpy
from rclpy.node import Node
from std_msg.msg import String


class AudioRecordingNode(Node):
    def __init__(self):
        super().__init__("audio_recording")
        # self.subscription = self.create_subscription(String, )


def main(args=None):
    rclpy.init(args=args)

    audio_recording_node = AudioRecordingNode()

    rclpy.spin(audio_recording_node)

    audio_recording_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
