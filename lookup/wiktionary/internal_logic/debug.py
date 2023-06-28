import time

_current_timer = 0


def debug_reset_timer():
    global _current_timer
    print("--new timer initiated--")
    _current_timer = time.perf_counter()


def debug_event_timer(name: str):
    global _current_timer
    _new_timer = time.perf_counter()
    print("{:.6f}: {}".format(_new_timer - _current_timer, name))
    _current_timer = _new_timer
