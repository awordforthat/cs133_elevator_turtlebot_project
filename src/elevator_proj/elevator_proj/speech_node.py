import os
import rclpy
import time

from pydub import AudioSegment


from pydub.playback import play
from rclpy.node import Node
from std_msgs.msg import String

from elevator_proj.constants import (
    HRI_TOPIC,
    FEEDBACK_TOPIC,
    ASSET_FOLDER,
    AUDIO_SUBDIR,
    COMMAND_AFFECT_HAPPY,
    COMMAND_AFFECT_SAD,
    COMMAND_NORMAL,
    COMMAND_UNUSUAL,
)


class SpeechNode(Node):
    def __init__(self):
        super().__init__("speech_node")
        self.subscription = self.create_subscription(
            String, HRI_TOPIC, self.callback, 10
        )
        self.feedback_publisher_ = self.create_publisher(String, FEEDBACK_TOPIC, 10)
        assets_path = os.path.expanduser(f"{ASSET_FOLDER}/{AUDIO_SUBDIR}")
        self.happy_normal_audio = AudioSegment.from_file(
            f"{assets_path}/happy_normal.mp3"
        )
        self.sad_normal_audio = AudioSegment.from_file(f"{assets_path}/sad_normal.mp3")
        self.happy_unusual_audio = AudioSegment.from_file(
            f"{assets_path}/happy_unusual.mp3"
        )
        self.sad_unusual_audio = AudioSegment.from_file(
            f"{assets_path}/sad_unusual.mp3"
        )

    def callback(self, msg):
        # TODO(echarles): figure out QoS so messages that come in during the
        # speaking phase don't interrupt the speech. Maybe we want a "cancel" behavior?
        self.get_logger().info(f"Speech node heard: {msg.data}")

        # This overeager checking is to prevent us from playing anything if a completely
        # unrelated message ends up being sent.
        is_happy = COMMAND_AFFECT_HAPPY in msg.data
        is_sad = COMMAND_AFFECT_SAD in msg.data
        is_normal = COMMAND_NORMAL in msg.data
        is_unusual = COMMAND_UNUSUAL in msg.data

        response = "Done"
        # These play commands are blocking.
        if is_happy and is_normal:
            play(self.happy_normal_audio)
        elif is_happy and is_unusual:
            play(self.happy_unusual_audio)
        elif is_sad and is_normal:
            play(self.sad_normal_audio)
        elif is_sad and is_unusual:
            play(self.sad_unusual_audio)
        else:
            response = "did not play audio"

        feedback = String()
        feedback.data = response
        self.feedback_publisher_.publish(feedback)


def main(args=None):
    rclpy.init(args=args)

    speech_node = SpeechNode()

    rclpy.spin(speech_node)

    speech_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
