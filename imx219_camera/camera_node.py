#!/usr/bin/env python3
"""
IMX219 Camera Node for ROS2 Humble
Captures RAW frames via v4l2-ctl and publishes as sensor_msgs/Image
Code by: y2k URL: https://github.com/unixfool
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import numpy as np
import cv2
import subprocess
import os
import time

class IMX219CameraNode(Node):

    def __init__(self):
        super().__init__('imx219_camera')

        self.declare_parameter('fps',      1)
        self.declare_parameter('scale',    0.25)
        self.declare_parameter('device',   '/dev/video0')
        self.declare_parameter('frame_id', 'camera')
        self.declare_parameter('exposure', 2495)

        self.fps      = self.get_parameter('fps').value
        self.scale    = self.get_parameter('scale').value
        self.device   = self.get_parameter('device').value
        self.frame_id = self.get_parameter('frame_id').value
        self.exposure = self.get_parameter('exposure').value

        self.width   = 3264
        self.height  = 2464
        self.raw_tmp = '/tmp/ros2_imx219_raw.bin'
        self.frame_count = 0
        self.error_count = 0

        self.pub_image = self.create_publisher(Image,      'camera/image_raw',   10)
        self.pub_info  = self.create_publisher(CameraInfo, 'camera/camera_info', 10)

        # Set exposure once at startup
        subprocess.run(['v4l2-ctl', f'--device={self.device}',
            f'--set-ctrl=exposure={self.exposure}'], capture_output=True, timeout=3)

        self.timer = self.create_timer(1.0 / self.fps, self.capture_and_publish)

        self.get_logger().info(
            f'IMX219 Camera Node started — '
            f'{self.width}x{self.height} scale={self.scale} '
            f'fps={self.fps} exposure={self.exposure}'
        )

    def capture_frame(self):
        # Remove stale tmp file
        if os.path.exists(self.raw_tmp):
            os.remove(self.raw_tmp)

        try:
            subprocess.run([
                'v4l2-ctl', f'--device={self.device}',
                f'--set-fmt-video=width={self.width},height={self.height},pixelformat=RG10',
                '--stream-mmap', '--stream-count=1',
                f'--stream-to={self.raw_tmp}'
            ], capture_output=True, timeout=15)
        except subprocess.TimeoutExpired:
            self.get_logger().warn('v4l2-ctl timeout — skipping frame')
            return None

        if not os.path.exists(self.raw_tmp) or os.path.getsize(self.raw_tmp) == 0:
            return None

        raw = np.fromfile(self.raw_tmp, dtype=np.uint16)
        frame = raw[:self.width * self.height].reshape(self.height, self.width)
        frame_norm = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        bgr = cv2.cvtColor(frame_norm, cv2.COLOR_BayerBG2BGR_EA)

        # White balance
        h, w = bgr.shape[:2]
        zone = bgr[h//4:h//2, w//3:2*w//3]
        b, g, r = cv2.split(bgr.astype(np.float32))
        ref = float(zone[:,:,1].mean())
        b = np.clip(b * (ref / (float(zone[:,:,0].mean()) + 1e-6)), 0, 255)
        r = np.clip(r * (ref / (float(zone[:,:,2].mean()) + 1e-6)), 0, 255)
        result_img = cv2.merge([b, g, r]).astype(np.uint8)

        # CLAHE
        lab = cv2.cvtColor(result_img, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        result_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # Scale
        if self.scale != 1.0:
            nw = int(self.width * self.scale)
            nh = int(self.height * self.scale)
            result_img = cv2.resize(result_img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

        if os.path.exists(self.raw_tmp):
            os.remove(self.raw_tmp)

        return result_img

    def capture_and_publish(self):
        try:
            frame = self.capture_frame()
            if frame is None:
                self.error_count += 1
                self.get_logger().warn(f'Frame capture failed (errors: {self.error_count})')
                return

            self.frame_count += 1
            now = self.get_clock().now().to_msg()
            h, w = frame.shape[:2]

            msg = Image()
            msg.header.stamp    = now
            msg.header.frame_id = self.frame_id
            msg.height          = h
            msg.width           = w
            msg.encoding        = 'bgr8'
            msg.step            = w * 3
            msg.data            = frame.tobytes()
            self.pub_image.publish(msg)

            info = CameraInfo()
            info.header = msg.header
            info.width  = w
            info.height = h
            self.pub_info.publish(info)

            self.get_logger().info(
                f'Frame #{self.frame_count} published {w}x{h}',
                throttle_duration_sec=5.0
            )

        except Exception as e:
            self.get_logger().error(f'Error: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = IMX219CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
