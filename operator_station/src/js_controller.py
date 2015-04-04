#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from js_state import Axis, Buttons
from sensor_msgs.msg import Joy

DEFAULT_JS_MAKER = "Elecom Wireless Gamepad"
DEFAULT_NODE_NAME = "js_controller"
DEFAULT_TOPIC_NAME = "joy"
DEFAULT_CONTROLLER_NAME = "main"


class JoyStickController(object):
    def __init__(self, topic_name, controller_name=None):
        self.dpad = Axis(0.0, 0.0)
        self.lstick = Axis(0.0, 0.0)
        self.rstick = Axis(0.0, 0.0)
        self.buttons = Buttons(rospy.get_param('~js_maker', DEFAULT_JS_MAKER), [0] * 13)

        self.is_active = False
        self.topic_name = topic_name
        if controller_name is not None:
            self.name = controller_name
        else:
            self.name = topic_name

    def joy_callback(self, joy_data):
        self.dpad.x = joy_data.axes[5]
        self.dpad.y = joy_data.axes[4]
        self.lstick.x = joy_data.axes[1]
        self.lstick.y = joy_data.axes[0]
        self.rstick.x = joy_data.axes[3]
        self.rstick.y = joy_data.axes[2]
        self.buttons = joy_data.buttons

    def activate(self):
        self.is_active = True
        rospy.Subscriber(self.topic_name, Joy, self.joy_callback)

    @property
    def state(self):
        return self.dpad, self.lstick, self.rstick, self.buttons


# -------------------------------------------------------------------------
if __name__ == '__main__':
    rospy.init_node(DEFAULT_NODE_NAME, anonymous=True)
    js_controller = JoyStickController(DEFAULT_TOPIC_NAME, DEFAULT_CONTROLLER_NAME)
    js_controller.activate()

    r = rospy.Rate(10)  # hz
    while not rospy.is_shutdown():
        print(js_controller.state)
        r.sleep()


