from ctypes import c_uint8
from datetime import datetime, timedelta
import threading
import time

from RPi import GPIO

from .common import DO_NOTHING, NOT_SUPPLIED


class Knob:

    def __init__(self, clk, dt, sw=None, min_=None, max_=None, default=0,
                 on_update=None, on_press=None, on_release=None):
        self.configure(default, min_, max_, on_update or DO_NOTHING,
                       on_press or DO_NOTHING, on_release or DO_NOTHING)
        self._setup_rotate(clk, dt)
        self._setup_click(sw)

    def configure(self, value=NOT_SUPPLIED, min_=NOT_SUPPLIED,
                  max_=NOT_SUPPLIED, on_update=NOT_SUPPLIED,
                  on_press=NOT_SUPPLIED, on_release=NOT_SUPPLIED):
        if value is not NOT_SUPPLIED:
            self._value = value
        if min_ is not NOT_SUPPLIED:
            self._min = min_
        if max_ is not NOT_SUPPLIED:
            self._max = max_
        if on_update is not NOT_SUPPLIED:
            self._on_update = on_update
        if on_press is not NOT_SUPPLIED:
            self._on_press = on_press
        if on_release is not NOT_SUPPLIED:
            self._on_release = on_release

    @property
    def is_pressed(self):
        return self._sw and self._is_pressed

    @property
    def is_long_pressed(self):
        return self._sw and self.pushed_duration.seconds > 3

    @property
    def pushed_duration(self):
        if not self.is_pressed or not self._last_pressed:
            return timedelta()
        return datetime.now() - self._last_pressed

    @property
    def value(self):
        return self._value

    def _setup_rotate(self, clk, dt):
        self._clk = clk
        self._dt = dt
        GPIO.setup(dt, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(clk, GPIO.IN, GPIO.PUD_UP)
        thread = threading.Thread(target=self._update_rotation)
        thread.daemon = True
        thread.start()

    def _update_rotation(self):
        # history = c_uint8(0)
        # while 1:
        #     time.sleep(0.01)
        #     history.value <<= 1
        #     history.value |= GPIO.input(self._clk)
        #     if history == 0x7F:
        #         self._rotated()
        clk_last = GPIO.input(self._clk)
        while 1:
            clk_state = GPIO.input(self._clk)
            dt_state = GPIO.input(self._dt)
            if clk_last != clk_state:
                self._rotated()
            clk_last = clk_state
            time.sleep(0.01)

    def _setup_click(self, sw):
        self._sw = sw
        self._is_pressed = False
        self._last_pressed = None
        self._last_released = None
        if sw:
            GPIO.setup(self._sw, GPIO.IN, GPIO.PUD_UP)
            GPIO.add_event_detect(
                sw, GPIO.BOTH, callback=lambda channel: self._click())

    def _click(self):
        now = datetime.now()
        if self._sw:
            sw_data = GPIO.input(self._sw)
            if sw_data == 0 and not self._is_pressed and (
                    not self._last_released or
                    self._last_released + timedelta(microseconds=30000) < now):
                self._on_press()
                self._is_pressed = True
                self._last_pressed = now
            elif sw_data != 0 and self._is_pressed:
                self._on_release()
                self._is_pressed = False
                self._last_released = now

    def _rotated(self):
        if GPIO.input(self._clk) == GPIO.input(self._dt):
            if self._max is None or (
                    self._max is not None and self._value < self._max):
                self._value = self._value + 1
                self._on_update(self._value)
        else:
            if self._min is None or (
                    self._min is not None and self._value > self._min):
                self._value = self._value - 1
                self._on_update(self._value)
