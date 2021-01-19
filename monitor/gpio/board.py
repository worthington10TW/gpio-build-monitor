#!/usr/bin/env python3

if __debug__:
    from monitor.gpio.Mock import GPIO
else:
    from RPi import GPIO

import logging
import asyncio

from .constants import Lights


class Board(object):
    def __enter__(self):
        logging.info('Setting up GPIO')
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setwarnings(False)

        self.pwm = {}
        for light in Lights:
            self.GPIO.setup(
                light.value,
                self.GPIO.OUT,
                initial=self.GPIO.LOW)

            self.pwm[light.value] = self.GPIO.PWM(
                light.value,
                100)

        self.tasks = {}

        return self

    def on(self, light: Lights):
        logging.debug(f'Light {light} turning on...')
        self.GPIO.output(light.value, self.GPIO.HIGH)
        logging.debug(f'Light {light} on')

    async def pulse(self, light: Lights):
        if light.value in self.tasks:
            logging.debug(f'Light {light} is already pulsing.')
            return

        dc = 0
        pwm = self.pwm.get(light.value)
        if pwm is None:
            logging.error(f'Failed to pulse light {light}')
            return

        pwm.start(dc)

        self.tasks[light.value] = asyncio.ensure_future(pulse(pwm))
        logging.debug(f'Light {light} pulsing...')
        await asyncio.sleep(0.001)

    def off(self, light: Lights):
        pwm = self.pwm.get(light.value)
        if pwm is not None:
            pwm.stop()

        task = self.tasks.get(light.value)
        if task is not None:
            task.cancel()
            self.tasks.pop(light.value)

        logging.debug(f'Light {light} turning off...')
        self.GPIO.output(light.value, self.GPIO.LOW)
        logging.debug(f'Light {light} off')

    def __exit__(self, type, value, traceback):
        # logging.info('Cleaning up pulses')
        # [task.cancel() for task in self.tasks]
        # del self.tasks

        logging.info('Cleaning up GPIO')
        self.GPIO.cleanup()


async def pulse(pwm):
    while True:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            await asyncio.sleep(0.05)
        for dc in range(95, 0, -5):
            pwm.ChangeDutyCycle(dc)
            await asyncio.sleep(0.05)
