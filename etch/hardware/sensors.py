from datetime import datetime, timedelta
from math import sqrt
from statistics import mean
import asyncio
import contextlib
import time

from qwiic_icm20948 import QwiicIcm20948

from ..common import DO_NOTHING, NOT_SUPPLIED


class Sensor:
    _OFFSET_SAMPLES = 100
    _DEFAULT_SHAKE_THRESHOLD = 3.5
    _DEFAULT_SHAKE_DELAY = 5

    def __init__(self, address):
        self._address = address
        self._sensor = QwiicIcm20948(address)
        self._sensor.begin()
        self._last_shake = None

        while 1:
            if self._sensor.dataReady():
                self._sensor.getAgmt()
                break
            time.sleep(0.1)
        self._offset = mean(
            [self._calc_accel(*self.accelerometer) for _ in range(self._OFFSET_SAMPLES)]
        )

        self.configure(
            on_shake=DO_NOTHING,
            shake_delay=self._DEFAULT_SHAKE_DELAY,
            shake_threshold=self._DEFAULT_SHAKE_THRESHOLD,
        )

        loop = asyncio.get_event_loop()
        loop.create_task(self._poll_raw_data())
        loop.create_task(self._poll_shake())

    async def _poll_raw_data(self):
        while True:
            if self._sensor.dataReady():
                self._sensor.getAgmt()
            await asyncio.sleep(0.5)

    def configure(
        self,
        on_shake=NOT_SUPPLIED,
        shake_delay=NOT_SUPPLIED,
        shake_threshold=NOT_SUPPLIED,
    ):
        if shake_delay is not NOT_SUPPLIED:
            self._shake_delay = timedelta(seconds=shake_delay)
        if shake_threshold is not NOT_SUPPLIED:
            self._shake_threshold = shake_threshold
        if on_shake is not NOT_SUPPLIED:
            self._on_shake = on_shake or DO_NOTHING

    @contextlib.contextmanager
    def config(self, **kwargs):
        # TODO: Create a stack to push values
        _push_on_shake = self._on_shake
        self.configure(**kwargs)
        try:
            yield self
        finally:
            self.configure(_push_on_shake)

    @property
    def temperature(self):
        return self._sensor.tmpRaw / 100

    @property
    def accelerometer(self):
        return (
            self._sensor.axRaw / 1000,
            self._sensor.ayRaw / 1000,
            self._sensor.azRaw / 1000,
        )

    @property
    def gyroscope(self):
        return (
            self._sensor.gxRaw / 1000,
            self._sensor.gyRaw / 1000,
            self._sensor.gzRaw / 1000,
        )

    @property
    def magnetometer(self):
        return (
            self._sensor.mxRaw,
            self._sensor.myRaw,
            self._sensor.mzRaw,
        )

    @property
    def acceleration(self):
        if not hasattr(self, "_offset"):
            self._offset = mean(
                [
                    self._calc_accel(*self.accelerometer)
                    for _ in range(self._OFFSET_SAMPLES)
                ]
            )
        x, y, z = self.accelerometer
        return abs(self._calc_accel(x, y, z) - self._offset)

    def _calc_accel(self, *args):
        return abs(sqrt(sum(i ** 2 for i in args)))

    async def _poll_shake(self):
        while 1:
            now = datetime.now()
            accel = self.acceleration
            if self.acceleration > self._shake_threshold and (
                not self._last_shake or now > self._last_shake + self._shake_delay
            ):
                self._last_shake = now
                self._on_shake(accel)
            else:
                await asyncio.sleep(0.01)
