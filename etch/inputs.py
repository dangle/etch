from RPi import GPIO


class Inputs:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._callbacks = []
        self._paused = False

    def __enter__(self):
        return self

    def __exit__(self, *_):
        GPIO.cleanup()
        self._callbacks = []

    def register(self, callback):
        if not self._paused and callback in self._callbacks:
            return
        self._callbacks.append(callback)
        pull = getattr(callback, 'pull', GPIO.PUD_OFF)
        GPIO.setup(callback.channels, GPIO.IN, pull_up_down=pull)
        detect = getattr(callback, 'detect', GPIO.BOTH)
        bounce = getattr(callback, 'bounce', 10)
        for channel in callback.channels:
            GPIO.add_event_detect(
                channel, detect, callback=callback, bouncetime=bounce)

    def pause(self):
        if self._paused:
            return
        self._paused = True
        for callback in self._callbacks:
            for channel in callback.channels:
                GPIO.remove_event_detect(channel)
        GPIO.cleanup()

    def resume(self):
        if not self._paused:
            return
        self._paused = False
        GPIO.setmode(GPIO.BCM)
        for callback in callbacks:
            self.register(callback)
