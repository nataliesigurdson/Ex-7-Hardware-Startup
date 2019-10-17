#!/usr/bin/python3

# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()

# For this example we will use the RPiMIB to create the PWM signals to talk to Servo Motors motor controllers.
#
# The RPiMIB (Raspberry Pi Multi Interface Board) has two PWM outputs, which will be sufficient for this example. If
# need more than 2 PWM outputs we typically use the Adafruit 16 Channel PWM module that uses the I2C bus on the RPi.
# More info on that later - but here is a sneak peak if you are interested
# https://learn.adafruit.com/16-channel-pwm-servo-driver?view=all
#
# The RPiMIB was a hardware and software project developed in conjuction with DPEA mentors, teachers and students.
# Joe Kleeburg a mentor for the DPEA, did the mechanical design of the circuit and PCB.
# Doug Whetter has taken the lead on firmware and software development.
# The RPiMIB has a couple of very specific goals:
# 1. Expand the available I/O on the Raspberry Pi, while the RPi is connected to a Slush engine which uses 99% of the
# built in RPi I/O
# 2. Enable the RPi to connect to 5V SPI and I2c buses (versus its native 3.3V SPI and I2c buses)
# 3. Provide battery backed up power to the RPi in the event of power loss, and gracefully shutdown the RPi.
#
# The above functionality if the RPiMIB is made possible primarily by the use of a Cypress Programmable System On a Chip
# (PSOC) which is basically a highly sophisticated programmable chip on the RPiMIB. This Chip has to be programmed with
# Firmware - then that firmware can be accessed by software written on the RPi. The Firmware is written in a combination
# of C++ and a proprietary hardware design language / user interface.
#
# The schematics and documentation for the RPiMIB is on github - search for the RPiMIB repo.
#
# So for a RPiMIB to work several things have to happen:
# 1. The board needs to be assembled correctly - we have DPEA electrical students working on these
# 2. The Cypress PSOC needs to have the correct firmware programmed on it - you can verify the firmware version from the
#    python library and print it to the screen, so you always know which version of the firmware you are using
# 3. The RPiMIB needs to be correctly assembled and plugged in to the RPi, Slush Engine and associated power supplies
# 4. The Software library needs to be correctly installed and kept up to date with updates. Fortunately the software
#    resides in RaspberryPiCommon Github repo which is something you should always keep up tp date.
#
# As mentioned, the Software library is in RaspberryPiCommon/pidev/Cyprus_Commands/Cyprus_Commands.py
# The code is readable - and there is a very well written readme with example usage in the same folder as the library.
#
# The PWM Ports on the RPiMIB are P4 and P5. The software library can be used to control both servo motors and motor
# controllers like the Talon that use a servo motor input and convert that to a high current drive that can control
# large motors.
#
# In addition to creating PWM that is used to control servo motors and servo motor style motor controllers the software
# library has been designed to also create non servo specific PWM for controlling industry standard motor controllers.
# Basically the Servo PWM is a special case of industry standard PWM, hopefully we will get to more on this later.
#

# To get a RC servo motor signal out of P4 of the RPiMIB do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
cyprus.setup_servo(1)  # sets up P4 on the RPiMIB as a RC servo style output
cyprus.set_servo_position(1, 0)  # 1 specifies port P4, 0 is a float from 0-1 that specifies servo position ~(0-180deg)
sleep(1) # wait one second for the servo to get there... minimum here should be about sleep(0.05)
cyprus.set_servo_position(1, .5)  # 1 specifies port P4, 0.5 specifies servo position ~(0-180deg) range of (0-1)
# when done disconnect the RPiMIB communication
cyprus.close()

# To get a RC servo motor CONTROLLER signal out of P5 of the RPiMIB do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
cyprus.setup_servo(2)  # sets up P5 on the RPiMIB as a RC servo motor controller style output
# for loop will set speed all the way from 0-full reverse to 0.5-halt to 1-full forward then halt with half second delays
for i in range(5, 10, 1):
    cyprus.set_servo_position(2, i/10.0)  # 2 specifies port P5, i is a float that specifies speed
    sleep(0.5)
cyprus.set_servo_position(1, 0.5)  # halt the motor
cyprus.close()  # when done disconnect the RPiMIB communication

# To get a Industrial PWM output on P5 to control something like a Cytron Motor Controller do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
# the following command will set up port 2 (P5) to put out a 100000HZ (100KHz) signal with a 50% high time or duty cycle
cyprus.set_pwm_values(2, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
# Motor controller Ex. Cytron MD10C connected to P5, the connected motor would be running ~50% max rpm
cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL) #  Motor OFF
cyprus.close()

# To get sensors and other I/O to work with RPiMIB