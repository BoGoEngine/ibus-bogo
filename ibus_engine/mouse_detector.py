import os
import sys

ENGINE_PATH = os.path.dirname(__file__)

sys.path.insert(0, os.path.abspath(os.path.join(ENGINE_PATH, "libs")))

from Xlib.display import Display as XDisplay
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

import threading
import ctypes
 
 
def _async_raise(tid, excobj):
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(excobj))
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
class Thread(threading.Thread):
    def raise_exc(self, excobj):
        assert self.isAlive(), "thread must be started"
        for tid, tobj in threading._active.items():
            if tobj is self:
                _async_raise(tid, excobj)
                return
        
        # the thread was alive when we entered the loop, but was not found 
        # in the dict, hence it must have been already terminated. should we raise
        # an exception here? silently ignore?
    
    def terminate(self):
        # must raise the SystemExit type, instead of a SystemExit() instance
        # due to a bug in PyThreadState_SetAsyncExc
        self.raise_exc(SystemExit)


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
        self.display = XDisplay()
        self.ctx = self.display.record_create_context(
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

        self.display.record_enable_context(self.ctx, self.handler)
        self.display.record_free_context(self.ctx)

    def handler(self, reply):
        data = reply.data
        while len(data):
            event, data = rq \
                .EventField(None) \
                .parse_binary_value(data, self.display.display, None, None)

            if event.type == X.ButtonRelease:
                for callback in self.callbacks:
                    callback()

    def add_mouse_click_listener(self, fn):
        self.callbacks.append(fn)
