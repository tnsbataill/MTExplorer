"""general view setup"""
from typing import TypedDict
from view.root import Root
from view.bombrowser import BomBrowserView
class Frames(TypedDict):
    """initialize frames class for window"""
    bombrowser: BomBrowserView

class View:
    """initialize general view class"""
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}

        self._add_frame(BomBrowserView, "bombrowser")

    def _add_frame(self, frame, name: str) -> None:
        self.frames[name] = frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        """frame changeover"""
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        "run mainloop for window"
        self.root.mainloop()
