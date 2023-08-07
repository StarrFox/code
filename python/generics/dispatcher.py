from typing import Callable
from collections import defaultdict, deque
import time


class Event: pass


class Start(Event):
    def start(self):
        return "started"


class End(Event):
    def end(self):
        return "ended"


class Dispatcher:
    def __init__(self) -> None:
        # I tried type hinting this dict for a long time
        self._listeners = defaultdict(list)
        self.event_queue: deque[Event] = deque()

    def loop(self):
        while True:
            event = self.event_queue.popleft()
            self._send_event(event)
            time.sleep(1)

    def _send_event(self, event: Event):
        for callback in self._listeners[type(event)]:
            callback(event)

    def dispatch(self, event: Event):
        self.event_queue.append(event)

    def add_listener[E: Event](self, event: type[E], callback: Callable[[E], object]):
        self._listeners[event].append(callback)

    def listen[E: Event](self, event: type[E]):
        def _inner(func: Callable[[E], object]):
            self.add_listener(event, func)
            return func

        return _inner


dispatch = Dispatcher()


@dispatch.listen(Start)
def listen_start(event: Start):
    print(f"Start! {event.start()}")
    return


@dispatch.listen(End)
def listen_end(event: End):
    print(f"End! {event.end()}")
    return 1


dispatch.dispatch(Start())
dispatch.dispatch(End())

dispatch.loop()
