import os
import sys
from threading import Thread

ENGINE_PATH = os.path.dirname(__file__)

sys.path.insert(0, os.path.abspath(os.path.join(ENGINE_PATH, "libs")))

from Xlib.display import Display as XDisplay
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq


class MouseDetector(Thread):
    def __init__(self):
        super().__init__()
        self.callbacks = []

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = MouseDetector()
        return cls._instance

    def run(self):
        display = XDisplay()
        self.display = display
        ctx = display.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.ButtonPressMask, X.ButtonReleaseMask),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])

        self.running = True
        display.record_enable_context(ctx, self.handler)
        display.record_free_context(ctx)

    def handler(self, reply):
        data = reply.data
        while len(data):
            if not self.running:
                break
            event, data = rq \
                .EventField(None) \
                .parse_binary_value(data, self.display.display, None, None)

            if event.type == X.ButtonRelease:
                for callback in self.callbacks:
                    callback()

    def stop(self):
        self._running = False

    def add_mouse_click_listener(self, fn):
        self.callbacks.append(fn)
