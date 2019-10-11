import os
import pygame

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.slider import Slider
from kivy.animation import Animation, AnimationTransition
from threading import Thread
from pidev.Joystick import Joystick
from time import sleep


from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
spi = spidev.SpiDev()


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)
STEPPER = stepper()
STEPPER.home(0)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
ctr = 1
Window.clearcolor = (1, 1, 1, 1)  # White


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

class MainScreen(Screen):
    mtrOnOff = ObjectProperty()
    def toggle(self):
        global ctr
        if ctr % 2 == 0:
            self.onOffBtn.text = "On"
            s0.start_relative_move(20)
            ctr += 1

        else:
            self.onOffBtn.text = "Off"
            s0.softStop()
            ctr += 1


"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()


