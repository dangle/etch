import asyncio

from ..app import App


class BootSequence(App):
    async def start(self) -> None:
        await self._display_logo()
        self.etch.blank(update=False)
        await self._display_instructions()

    async def _display_logo(self):
        self.etch.set_display_mode(self.etch.modes.A2)
        self.etch.text("Etch", font="Magic", size=200, y=400, update=False)
        self.etch.text("- a -", font="Magic", size=200, y=600, update=False)
        self.etch.text("Sketch", font="Magic", size=200, y=800)
        await asyncio.sleep(5)

    async def _display_instructions(self):
        self.etch.refresh()
