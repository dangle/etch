from IT8951.constants import DisplayModes


class Pong:
    def __init__(self) -> None:
        self._etch = None

    async def __call__(self, etch) -> None:
        self._etch = etch
        self._etch.set_display_mode(DisplayModes.DU)
        self._etch.blank()
        self._etch.refresh()


pong = Pong()
