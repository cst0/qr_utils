#!/usr/bin/env python3
import rospy
import time
#import sys
#sys.path.insert(1, '~/.local/lib/python2.7/site-packages/cv2/')
#__requires__="opencv-python==4.2.0.32"
#import pkg_resources
#pkg_resources.require("opencv-python==4.2.0.32")
import cv2

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from qr_utils.srv import ReadEnvironment, ReadEnvironmentResponse

BRIDGE = CvBridge()
DETECTOR = cv2.QRCodeDetector()

IMAGE = None
MOST_RECENT_TIME = 0

def image_read(image):
    global IMAGE
    IMAGE = image

def handle_read_env(req):
    req.empty  # input is empty, ignore
    global IMAGE
    if IMAGE is None:
        return ReadEnvironmentResponse([''])

    start_reads = time.time()
    sample_timing = 2
    text = []
    while time.time() - start_reads < sample_timing:
        cv_image = BRIDGE.imgmsg_to_cv2(IMAGE)
        res = (DETECTOR.detectAndDecode(cv_image))
        text, _, _ = res

    rospy.loginfo("Reading didn't match any known inputs!")
    return ReadEnvironmentResponse(text)

def read_env_server():
    rospy.init_node('read_environment_server')
    global MOST_RECENT_TIME
    MOST_RECENT_TIME = time.time()
    rospy.Subscriber('/camera/color/image_raw', Image, image_read)
    s = rospy.Service('/qr_reader/read_environment', ReadEnvironment, handle_read_env)
    print("Ready to read your env.")
    rospy.spin()
    s.shutdown()

if __name__ == "__main__":
    read_env_server()

