import os

import cv2
import numpy as np

from elevator_proj.constants import (
    COMMAND_QR,
    HRI_TOPIC,
    COMMAND_AFFECT_HAPPY,
    COMMAND_AFFECT_SAD,
    ASSET_FOLDER,
    IMAGES_SUBDIR,
    COMMAND_CLEAR,
)
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ScreenNode(Node):
    def __init__(self):
        super().__init__("screen_node")
        self.subscription = self.create_subscription(
            String, HRI_TOPIC, self.callback, 10
        )

        # TODO(echarles): use path library properly
        assets_path = os.path.expanduser(f"{ASSET_FOLDER}/{IMAGES_SUBDIR}")

        self.current_image = None
        self.happy_image = cv2.imread(f"{assets_path}/happy.png")
        self.sad_image = cv2.imread(f"{assets_path}/sad.png")
        self.qr_code = cv2.imread(f"{assets_path}/qr-code.png")

        h, w = self.happy_image.shape[:2]
        self.blank = np.zeros((h, w, 3), dtype=np.uint8)

        if self.happy_image is None:
            raise FileNotFoundError(f"happy image not found in folder {assets_path}")

        if self.sad_image is None:
            raise FileNotFoundError(f"sad image not found in folder {assets_path}")

        if self.qr_code is None:
            raise FileNotFoundError(f"qr code not found in folder {assets_path}")

        cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("img", cv2.WND_PROP_TOPMOST, 1)

        cv2.resizeWindow("Display", w, h)

        self.get_logger().info("loaded files")
        self.timer = self.create_timer(0.03, self.refresh)

    def callback(self, msg):
        self.get_logger().info(f"Screen node heard: {msg.data}")
        if COMMAND_AFFECT_HAPPY in msg.data:
            self.current_image = self.happy_image
            print("HAPPY!")
        elif COMMAND_AFFECT_SAD in msg.data:
            self.current_image = self.sad_image
            print("SAD :(")
        elif COMMAND_QR in msg.data:
            self.current_image = self.qr_code
        elif COMMAND_CLEAR in msg.data:
            self.current_image = self.blank

    def refresh(self):
        cv2.waitKey(1)
        if self.current_image is not None:
            cv2.imshow("Display", self.current_image)

    def test(self):
        cv2.imshow("Display", self.happy_image)


def main(args=None):
    rclpy.init(args=args)

    speech_node = ScreenNode()

    rclpy.spin(speech_node)

    speech_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
