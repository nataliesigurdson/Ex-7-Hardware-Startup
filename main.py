import os
import pygame
import spidev

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
import RPi.GPIO as GPIO
from pidev.stepper import stepper
import time


from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
TRANSITION_SCREEN_NAME = 'TransitionScreen'
ctr = 1
ctr2 = 0
ctr3 = 1
ctr4 = 0
joystick = Joystick(0, True)
STEPPER = stepper()
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)


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


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    onOffBtn = ObjectProperty(None)
    ctrBtn = ObjectProperty(None)
    mtrBtn = ObjectProperty(None)
    # motorLabel = ObjectProperty(None)
    flip = ObjectProperty(None)
    slider = ObjectProperty(None)
    imageBtn = ObjectProperty(None)
    pratik2 = ObjectProperty(None)
    joy_y_val = ObjectProperty()
    joy_x_val = ObjectProperty()
    mtrOnOff = ObjectProperty()
    speedSlider = ObjectProperty()
    txt_var1 = ObjectProperty()
    txt_var2 = ObjectProperty()
    fancyPosition = ObjectProperty()

    button_state_var = False





    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def toggle(self):
        global ctr  # button_state_var
        # self.button_state_var=button_state_var
        if ctr % 2 != 0:
            self.onOffBtn.text = ""
            ctr += 1

        else:
            self.onOffBtn.text = "Toggle"
            ctr += 1

    def counter(self):
        global ctr2
        if ctr2 < 1:
            ctr2 += 1
            self.ctrBtn.text = str(ctr2)
        else:
            ctr2 += 1
            self.ctrBtn.text = str(ctr2)

    def transitionto(self):
        SCREEN_MANAGER.current = TRANSITION_SCREEN_NAME

    def animate(self):
        anim = Animation(x=50) + Animation(size=(80, 80), duration=2.)
        anim.start(self.ids.animate_pratik)

    def joy_update(self):  # This should be inside the MainScreen Class
        while True:
            self.joy_x_val = joystick.get_axis('x')
            self.ids.joy_label_x.x = (self.joy_x_val)
            self.joy_y_val = joystick.get_axis('y')
            self.ids.joy_label_y.y = (self.joy_y_val)
            for x in range(11):
                if joystick.get_button_state(x) == 1:
                    self.ids.jButton.text = str(x+1)
                    break
                else:
                    self.ids.jButton.text = str(0)

            sleep(.1)

    def start_joy_thread(self):  # This should be inside the MainScreen Class
        Thread(target=self.joy_update).start()

    def toggle2(self):
        # global ctr3
        # if ctr3 % 2 == 0:
        #    self.onOffBtn.text = "On"
        #    s0.start_relative_move(20)
        #   ctr3 += 1

        # else:
        #    self.onOffBtn.text = "Off"
        #    s0.softStop()
        #    ctr3 += 1
        global ctr4
        print("toggle2")
        # if ctr4 % 2 == 0:
        if s0.is_busy():
            print("motor busy")
            s0.softStop()
            self.mtrOnOff.text = "Motor Off"
            # ctr4 += 1

        else:
            s0.start_relative_move(20)
            self.mtrOnOff.text = "Motor On"
            print("motor not busy")
            # ctr4 += 1

    def change_direction(self):
        global ctr4
        if ctr4 % 2 == 0:
            print("going counterclockwise")
            s0.stop()
            s0.start_relative_move(-20)
            self.changeDir.text = "Go Counterclockwise"
            ctr4 += 1

        else:
            s0.stop()
            s0.start_relative_move(20)
            self.changeDir.text = "Go Clockwise"
            print("going clockwise")
            ctr4 += 1

    def slider2(self):
        global s0
        s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                     steps_per_unit=200, speed=self.speedSlider.value)
        s0.start_relative_move(20)

    def fancy_button(self):
        global s0
        txt_var1 = s0.get_position_in_units()
        s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                     steps_per_unit=200, speed=5)
        s0.relative_move(15)
        self.fancyPosition.text = "current position: %d " % s0.get_position_in_units()
        time.sleep(5)  # some speed values are increased and sleeps time decreased temporarily so code will run faster
        self.ids.speed = 6
        s0.relative_move(10)
        self.fancyPosition.text = "current position: %d " % s0.get_position_in_units()



class TransitionScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('TransitionScreen.kv')
        super(TransitionScreen, self).__init__(**kwargs)

    def transitionback(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def animate(self):
        anim = Animation(x=50) + Animation(size=(80, 80), duration=2.)
        anim.start(self.ids.pratik2)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

        self.flip = False

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(TransitionScreen(name=TRANSITION_SCREEN_NAME))


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
